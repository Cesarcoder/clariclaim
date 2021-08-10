class Message < ApplicationRecord
  enum category: [:sms, :email]
end
