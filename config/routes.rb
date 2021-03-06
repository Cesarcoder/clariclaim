Rails.application.routes.draw do

  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)

  resources :claims do
    collection do
      get :success
      post :insurance_estimate
      post :extract # mock
    end

    member do
      get :export
      post :review
      resources :charges, only: [:new, :create]
    end
  end

  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  root 'home#index'

  get '/revamp', to: 'home#revamp'
end
