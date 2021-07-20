class Claim < ApplicationRecord
  extend ActiveHash::Associations::ActiveRecordExtensions

  enum contact_preference: { phone: 0, email: 1 }

  belongs_to :package
  has_one_attached :policy_limit
  has_one_attached :insurance_estimate

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
