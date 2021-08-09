class ClaimsController < ApplicationController
  def create
    @claim = Claim.new(claim_params)

    respond_to do |format|
      if @claim.save
        @claim.update_columns(
          addons_data: addons_params,
          loss_location_meta: loss_location_meta_params
        )

        ExtractWorker.perform_async(@claim.id)

        format.html { redirect_to success_claims_path, notice: "Claim was successfully created." }
        format.json { render :show, status: :created, location: @claim }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @claim.errors, status: :unprocessable_entity }
      end
    end
  end

  def success; end

  def insurance_estimate
    FileUtils.cp(params[:file].tempfile.path, "#{Rails.root}/pdfparserapi/pdfs/")

    temp_filename = params[:file].tempfile.path.split("/").last

    require 'uri'
    require 'net/http'

    uri = URI(ENV['OCR_SERVICE_URL'])
    https = Net::HTTP.new(uri.host, uri.port)
    https.read_timeout = 1_000

    request = Net::HTTP::Post.new(uri.path)
    request["Content-Type"] = "application/json"
    request.body = {
      pdf_path: "/pdfs/#{temp_filename}"
    }.to_json

    response = https.request(request)
    budget = JSON.parse(response.body)['data']['RCV'] rescue nil

    render json: { data: Package.find_package(budget).try(:id), status: :ok }
  end

  def extract
    puts "extracted"
    render json: {
      "RCV": "40433.49",
      "business": "(508) 450-0507 (508) 450-0507",
      "claim_number": "TPPT84",
      "company": "",
      "email": "tim.martino@seltser.com espalding@mapfreusa.com espalding@mapfreusa.com",
      "estimate": "BILLY_SILVA",
      "estimator": "Erin Spalding",
      "insured": "BILLY SILVA",
      "phone": "",
      "policy_number": "BHMVBV",
      "type_of_loss": "Water Damage"
    }
  end

  private
    # Only allow a list of trusted parameters through.
    def claim_params
      params.require(:claim).permit(
        :loss_type, :loss_date, :loss_type_desc, :property_type,
        :other_unit_affected, :loss_location, :loss_location_point,
        :declarations_page, :insurance_estimate,
        :damage_outside_insurance, :package_id, :addons_data, :first_name,
        :last_name, :address, :city, :state, :zipcode, :phone, :email,
        :contact_preference
      )
    end

    def addons_params
      ids = params[:claim].slice(:addons_101, :addons_102, :addons_103)
                  .values.compact.map(&:to_i)
      rooms = []
      params[:claim][:room_name].each_with_index do |name, index|
        rooms << {
          name: name,
          dimension: params[:claim][:room_dimension][index]
        }
      end if ids.include?(101)

      {
        ids: ids,
        supplemental_claims: {
          rooms: rooms
        }
      }
    end

    def loss_location_meta_params
      JSON.parse(params[:claim][:loss_location_meta])
    end
end
