class ZohoService
  include HTTParty

  def initialize
    @client_id     = Rails.application.credentials.zoho[:client_id]
    @client_secret = Rails.application.credentials.zoho[:client_secret]
    @refresh_token = Rails.application.credentials.zoho[:refresh_token]
    @redirect_uri  = 'http://clariclaim.com'
  end

  def oauth_token
    params = {
      client_id:     @client_id,
      client_secret: @client_secret,
      refresh_token: @refresh_token,
      grant_type:    'refresh_token'
    }
    url = "https://accounts.zoho.com/oauth/v2/token?#{params.to_query}"
    response = self.class.post(url)
    response.parsed_response['access_token']
  end

  def create_lead params, access_token
    url = 'https://www.zohoapis.com/crm/v2/Leads'

    response = self.class.post(url, options_from(params, access_token))
  end

  def create_contact params, access_token
    url = 'https://www.zohoapis.com/crm/v2/Contacts'

    response = self.class.post(url, options_from(params, access_token))
  end

  def find_contact first_name, last_name, access_token
    url = "https://www.zohoapis.com/crm/v2/Contacts/search?criteria=((Last_Name:equals:#{last_name})and(First_Name:equals:#{first_name}))"

    response = self.class.get(url, options_from({}, access_token))
    response.parsed_response
  end

  def create_deal params, access_token
    url = 'https://www.zohoapis.com/crm/v2/Deals'

    response = self.class.post(url, options_from(params, access_token))
  end

  def options_from params, access_token
    {
      headers: {
        Authorization: "Zoho-oauthtoken #{access_token}"
      },
      body: params.to_json
    }
  end
end
