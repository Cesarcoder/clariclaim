class CreateClaims < ActiveRecord::Migration[6.1]
  def change
    create_table :claims do |t|
      t.string  :loss_type
      t.text    :loss_type_desc
      t.string  :loss_location
      t.string  :loss_location_point
      t.date    :loss_date
      t.string  :property_type
      t.boolean :other_unit_affected
      t.boolean :damage_outside_insurance
      t.integer :package_id
      t.json    :addons_data
      t.string  :first_name
      t.string  :last_name
      t.text    :address
      t.string  :city
      t.string  :state
      t.string  :zipcode
      t.string  :phone
      t.string  :email
      t.integer :contact_preference

      t.timestamps
    end

    add_index :claims, :package_id
  end
end
