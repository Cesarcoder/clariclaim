class ZohoDealCreator
  include Sidekiq::Worker

  def perform params, oauth_token
    # find contact by first name and last name
    zoho_service = ZohoService.new
    contact = zoho_service.find_contact(params[:first_name], params[:last_name], oauth_token)
    deal_params = {
      data:[{
        First_Name: params[:first_name],
        Last_Name: params[:last_name],
        Loss_Date: params[:loss_date],
        Property_Type: params[:property_type],
        Origin_Of_Loss: params[:loss_location_start],
        Documents: params[:insurance_estimate],
        Deal_Name: "#{params[:state]} #{params[:last_name]} #{params[:loss_type]}", # required field
        Type: params[:loss_type], # required field
        Pipeline: 'Standard (Standard)', # required field
        Stage: 'Prospect', # required field
        Contact: contact['data'].first['id'], # required field
        City: params[:city],
        State: params[:state],
        Address: params[:address],
        Zipcode: params[:zipcode]
      }]
    }
    zoho_service.create_deal(deal_params, oauth_token)
  end
end
