class Claim < ApplicationRecord
  extend ActiveHash::Associations::ActiveRecordExtensions

  enum contact_preference: { phone: 0, email: 1 }

  belongs_to :package

  mount_uploader :declarations_page,  PdfUploader
  mount_uploader :insurance_estimate, PdfUploader

  validate :loss_date_cannot_be_in_the_future

  after_initialize :set_default_json_data

  delegate :name, to: :package, prefix: true, allow_nil: true

  attribute :full_name

  def loss_type_formatted
    if loss_type_desc.present?
      "#{loss_type} - #{loss_type_desc}"
    else
      loss_type
    end
  end

  def addons
    Package.where(id: addons_ids)
  end

  def addons_ids
    addons_data.fetch('ids') rescue []
  end

  def update_addons(ids)
    self.addons_data['ids'] = ids.kind_of?(Array) ? ids : [ids]
    self.save!
  end

  def supplemental_claims
    addons_data.fetch('supplemental_claims') rescue []
  end

  def supplemental_rooms
    supplemental_claims.fetch('rooms') rescue []
  end

  def extract!
    require 'uri'
    require 'net/http'
    doc = insurance_estimate
    doc.cache_stored_file! if !doc.cached?

    uri = URI(ENV['OCR_SERVICE_URL'])
    https = Net::HTTP.new(uri.host, uri.port)
    https.read_timeout = 1_000
    # https.use_ssl = true

    request = Net::HTTP::Post.new(uri.path)
    request["Content-Type"] = "application/json"
    request.body = {
      pdf_path: doc.current_path.split("pdfparserapi")[1]
    }.to_json

    response = https.request(request)
    update_columns(meta: JSON.parse(response.body))
  end

  def send_sms(message, from=nil)
    require 'rubygems'
    require 'twilio-ruby'

    account_sid = 'AC38d806a071041dec24bcc491b6ed7e1c'
    auth_token = '[AuthToken]'
    @client = Twilio::REST::Client.new(account_sid, auth_token)
    @client.messages.create(
               body: message,
               to: phone_with_codes
             )

    puts message.sid
  end

  def phone_with_codes
    if !loss_location.include?("+")
      return phone.prepend("+1") if loss_location.include?("US")
    end

    phone
  end

  def meta_claim_number
    meta['data']['claim_number'] rescue ''
  end

  def meta_policy_number
    meta['data']['policy_number'] rescue ''
  end

  def meta_loss_type
    type_of_loss = meta['data']['type_of_loss'] rescue ''

    type_of_loss.present? ? type_of_loss : loss_type
  end

  def meta_insured
    meta['data']['insured'] rescue ''
  end

  def meta_estimator
    meta['data']['estimator'] rescue ''
  end

  def review_claim_number
    review_data['claim_number'] rescue meta_claim_number
  end

  def review_policy_number
    review_data['policy_number'] rescue meta_policy_number
  end

  def review_loss_type
    review_data['loss_type'] rescue meta_loss_type
  end

  def review_loss_date
    review_data['loss_date'] rescue loss_date
  end

  def insured
    "#{first_name} #{last_name}"
  end

  private

  def loss_date_cannot_be_in_the_future
    if loss_date.present? && loss_date > Date.today
      errors.add(:loss_date, "can't be in the future")
    end
  end

  def set_default_json_data
    addons_data = {} if addons_data.nil?
    review_data = {} if review_data.nil?
  end

  def full_name= value
    names = value.split(' ')
    if names.length > 1
      self.first_name = names[0]
      self.last_name  = value.from(names[0].length + 1)
    else
      self.first_name = ''
      self.last_name  = names[0]
    end
  end
end
