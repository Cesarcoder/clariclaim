class ZohoLeadCreator
  include Sidekiq::Worker

  def perform params, oauth_token
    lead_params = {
      data: [{
        Email: params[:email],
        Address: params[:address],
        Loss_Type: params[:loss_type],
        First_Name: params[:first_name],
        Last_Name: params[:last_name], # this is required field in zoho lead
        Company: params[:state] # this is required field in zoho lead
      }]
    }
    ZohoService.new.create_lead(lead_params, oauth_token)
  end
end
