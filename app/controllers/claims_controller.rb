class ClaimsController < ApplicationController
  def create
    @claim = Claim.new(claim_params)

    respond_to do |format|
      if @claim.save
        # after save
        @claim.update_columns(addons_data: addons_params)
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

  def extract
    puts "extracted"
    render json: {
       "claim_number":"TPPT84",
       "company":"Seltser & Goldstein Public Adjusters",
       "type_of_loss":"Water Damage",
       "insured":"Billy & Katie S",
       "estimate":"SILVA",
       "estimator":"Tim Martino",
       "email":"sample@email.com",
       "phone":"123123123"
    }
  end

  private
    # Only allow a list of trusted parameters through.
    def claim_params
      params.require(:claim).permit(
        :loss_type, :loss_date, :loss_type_desc, :property_type,
        :other_unit_affected, :loss_location, :location, :location_point,
        :declarations_page, :insurance_estimate, :damage_outside_insurance,
        :package_id, :addons_data,
        :first_name, :last_name, :address,
        :city, :state, :zipcode, :phone, :email, :contact_preference
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
end
