class AddReviewDataToClaim < ActiveRecord::Migration[6.1]
  def change
    add_column :claims, :review_data, :json
  end
end
