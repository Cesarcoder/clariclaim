class QuotesController < ApplicationController
  def create
    @quote = Quote.new(quote_params)

    respond_to do |format|
      if @quote.save
        @quote.update_columns(addons_data: addons_params)
        format.html { redirect_to success_quotes_path, notice: "Quote was successfully created." }
        format.json { render :show, status: :created, location: @quote }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @quote.errors, status: :unprocessable_entity }
      end
    end
  end

  def success; end

  private
    # Only allow a list of trusted parameters through.
    def quote_params
      params.require(:quote).permit(
        :loss_type, :loss_date, :loss_type_desc, :property_type,
        :other_unit_affected, :loss_location, :location, :location_point,
        :policy_limit, :insurance_estimate, :damage_outside_insurance,
        :package_id, :addons_data,
        :first_name, :last_name, :address,
        :city, :state, :zipcode, :phone, :email, :contact_preference
      )
    end

    def addons_params
      ids = params[:quote].slice(:addons_101, :addons_102, :addons_103)
                  .values.compact.map(&:to_i)
      rooms = []
      params[:quote][:room_name].each_with_index do |name, index|
        rooms << {
          name: name,
          dimension: params[:quote][:room_dimension][index]
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
