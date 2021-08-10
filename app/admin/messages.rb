ActiveAdmin.register Message do
  menu priority: 2

  actions :index, :show

  filter :to
  filter :created_at
  filter :category, as: :select, collection: Message.categories
end
