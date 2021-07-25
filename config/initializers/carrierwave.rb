CarrierWave.configure do |config|
    config.fog_provider = 'fog/google'
    config.fog_credentials = {
        provider:               'Google',
        google_project:         'clariclaim',
        google_json_key_string: Rails.application.credentials.gcs.to_json
    }
    config.fog_directory = ENV['BUCKET_NAME']
end
