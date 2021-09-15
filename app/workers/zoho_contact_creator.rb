class ZohoContactCreator
  include Sidekiq::Worker

  def perform params, oauth_token
    contact_params = {
      data: [{
        First_Name: params[:first_name],
        Last_Name: params[:last_name],
        Loss_Date: params[:loss_date],
        Property_Type: params[:property_type],
        Origin_Of_Loss: params[:loss_location_start],
        Documents: params[:insurance_estimate]
      }]
    }
    ZohoService.new.create_contact(contact_params, oauth_token)
  end
end
