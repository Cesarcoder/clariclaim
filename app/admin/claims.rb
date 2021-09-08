ActiveAdmin.register Claim do
  menu priority: 1

  actions :index, :show

  filter :first_name
  filter :package, collection: -> { Package.main }
  filter :loss_type
  filter :property_type
  filter :loss_location
  filter :created_at

  member_action :meta, method: :get do
    @meta = Claim.find(params[:id]).meta
  end

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
          row :loss_location_point do |claim|
            link_to(
              claim.loss_location_point,
              "https://maps.google.com/?q=#{claim.loss_location}&zoom=14",
              target: :_blank
            ) if claim.loss_location_point.present?
          end
          row "Loss Start" do |claim|
           claim.loss_location_start
          end
          row :loss_date
          row :property_type
          row :declarations_page do |claim|
            link_to(
              claim.declarations_page_identifier, claim.declarations_page.url,
              target: :_blank
            ) if !claim.declarations_page.file.nil?
          end
          row :insurance_estimate do |claim|
            link_to(
              claim.insurance_estimate_identifier, claim.insurance_estimate.url,
              target: :_blank
            ) if !claim.insurance_estimate.file.nil?
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

        # panel "Direct Contact" do
        #   div do
        #     html = ""
        #     html += div text_area(:message, :content, { style: 'width: 100%;', rows: 8, placeholder: "Your message here...", ontype: 'alert(sdsd)' }).html_safe
        #     html += br
        #     html += button("Send as SMS").html_safe
        #     html += button("<a href='#0' style='color: white;text-decoration: none;'> Send as Email</a>".html_safe, { style: 'float: right; color: white;'}).html_safe
        #     html
        #   end
        # end

        panel "Reviews" do
          attributes_table_for claim do
            render partial: 'review', locals: {
              claim: claim
            }
          end
        end
      end

      column do
        panel "Claim Meta" do
          attributes_table_for claim do
            claim&.meta["data"]&.each do |key, val|
              row key.to_sym do
                data = val
                if key == 'RCV'
                  data += " - ("
                  data += link_to(
                        "view details",
                        meta_admin_claim_path,
                        target: :_blank
                      )
                  data += ")"
                end

                data.html_safe
              end
            end
          end
        end if claim.meta && !claim.meta.empty?

        panel "Street View Maps" do
          attributes_table_for claim do
            render partial: 'maps', locals: {
              location: claim.loss_location,
              location_point: claim.loss_location_point
            }
          end
        end

        panel "Payment" do
          attributes_table_for claim do
            render partial: 'payment'
          end
        end
      end
    end
  end
end
