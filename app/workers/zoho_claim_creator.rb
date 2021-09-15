class ZohoClaimCreator
  include Sidekiq::Worker

  def perform params
    oauth_token = ZohoService.new.oauth_token
    ZohoLeadCreator.new.perform(params, oauth_token)
    ZohoDealCreator.new.perform(params, oauth_token)
    ZohoContactCreator.new.perform(params, oauth_token)
  end
end
