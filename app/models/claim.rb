class Claim < ApplicationRecord
  extend ActiveHash::Associations::ActiveRecordExtensions

  enum contact_preference: { phone: 0, email: 1 }

  belongs_to :package

  mount_uploader :declarations_page,  PdfUploader
  mount_uploader :insurance_estimate, PdfUploader

  validate :loss_date_cannot_be_in_the_future

  after_initialize :set_addons_data

  delegate :name, to: :package, prefix: true, allow_nil: true

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

    uri = URI(ENV['OCR_SERVICE_URL'])
    https = Net::HTTP.new(uri.host, uri.port)
    https.use_ssl = true

    request = Net::HTTP::Post.new(uri.path)

    puts "declarations_page.url"
    puts declarations_page.url

    request['file_url'] = declarations_page.url
    response = https.request(request)

    update_columns(meta: JSON.parse(response.body))
  end

  private

  def loss_date_cannot_be_in_the_future
    if loss_date.present? && loss_date > Date.today
      errors.add(:loss_date, "can't be in the future")
    end
  end

  def set_addons_data
    addons_data = {} if addons_data.nil?
  end
end
