class ExtractWorker
  include Sidekiq::Worker

  def perform(id)
    claim = Claim.find_by(id: id)
    claim.extract!
  end
end
