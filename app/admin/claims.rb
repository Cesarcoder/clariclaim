ActiveAdmin.register Claim do
  menu priority: 1

  actions :index, :show

  filter :first_name
  filter :loss_type
  filter :property_type
  filter :created_at

  index do
    id_column
    column :first_name
    column :package do |claim|
      claim.package_name
    end
    column :loss_type
    column :property_type
    column :other_unit_affected
    column :created_at
    actions
  end

  show do
    attributes_table do
      row :loss_type do |claim|
        claim.loss_type_formatted
      end
      row :loss_location
      # row :loss_location_point
      row :loss_date
      row :property_type
      row :policy_limit do |claim|
        link_to(
          claim.policy_limit.filename, url_for(claim.policy_limit),
          target: :blank
        ) rescue ""
      end
      row :insurance_estimate do |claim|
        link_to(
          claim.insurance_estimate.filename, url_for(claim.insurance_estimate),
          target: :blank
        ) rescue ""
      end
      row :other_unit_affected
      row :damage_outside_insurance
      row :package do |claim|
        claim.package_name
      end
      row :addons do |claim|
        addons = ""
        claim.addons.each do |addon|
          addons = li addon.name
        end
        addons
      end
      row :supplemental_claims do |claim|
        rooms = ""
        claim.supplemental_rooms.each do |room|
          rooms = li "#{room['name']} - #{room['dimension']}"
        end
        rooms
      end
      row :first_name
      row :last_name
      row :address
      row :city
      row :state
      row :zipcode
      row :phone
      row :email
      row :contact_preference
      row :created_at
    end
  end
end
