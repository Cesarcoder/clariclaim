ActiveAdmin.register Claim do
  menu priority: 1

  actions :index, :show

  filter :first_name
  filter :package, collection: -> { Package.main }
  filter :loss_type
  filter :property_type
  filter :loss_location
  filter :created_at

  index do
    id_column
    column :first_name
    column :package do |claim|
      claim.package_name
    end
    column :loss_type
    column :property_type
    column :loss_location
    column :created_at
    actions
  end

  show do
    columns do
      column do
        attributes_table do
          row :loss_type do |claim|
            claim.loss_type_formatted
          end
          row :loss_location
          row :loss_date
          row :property_type
          row :declarations_page do |claim|
            link_to(
              claim.declarations_page.filename, url_for(claim.declarations_page),
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

      column do
        panel "Claim Meta" do
          attributes_table_for claim do
            claim&.meta&.each do |key, val|
              row key.to_sym do
                val
              end
            end
          end
        end if claim.meta && !claim.meta.empty?

        panel "Street View Maps" do
          attributes_table_for claim do
            render partial: 'maps', locals: { location: claim.loss_location }
          end
        end

        panel "Direct Contact" do
          div do
            html = ""
            html += div text_area(:message, :content, { style: 'width: 100%;', rows: 8 }).html_safe
            html += br
            html += button("Send SMS").html_safe
            html += button("Send Email", { style: 'float: right;' } ).html_safe
            html
          end
        end
      end
    end
  end
end
