class CreateMessages < ActiveRecord::Migration[6.1]
  def change
    create_table :messages do |t|
      t.text :content
      t.string :to
      t.integer :category

      t.timestamps
    end
    add_index :messages, :category
  end
end
