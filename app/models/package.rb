class Package < ActiveHash::Base
  self.data = [
    {
      id: 1,
      name: "1-$1,000",
      price_range: 1..1_000,
      price_text: "$39.99",
      type: "main"
    },
    {
      id: 2,
      name: "$1,000-$2,500",
      price_range: 1_000..2_500,
      price_text: "$49.99",
      type: "main"
    },
    {
      id: 3,
      name: "$2,500-$5,000",
      price_range: 2_500..5_000,
      price_text: "$59.99",
      type: "main"
    },
    {
      id: 4,
      name: "$5,000-$15,000",
      price_range: 5_000..15_000,
      price_text: "$69.99",
      type: "main"
    },
    {
      id: 5,
      name: "$15,000-$30,000",
      price_range: 15_000..30_000,
      price_text: "$79.99",
      type: "main"
    },
    {
      id: 6,
      name: "$30,000-$50,000",
      price_range: 30_000..50_000,
      price_text: "$89.99",
      type: "main"
    },
    {
      id: 101,
      name: "Sumplemental Claim",
      price_text: "$199.99",
      type: "addons"
    },
    {
      id: 102,
      name: "20 Min Consultation",
      price_text: "$129.99",
      type: "addons"
    },
    {
      id: 103,
      name: "Will Refer a Qualified Public Adjuster In Your Area",
      price_text: "FREE",
      type: "addons"
    }
  ]

  def self.main
    where(type: "main")
  end

  def self.addons
    where(type: "addons")
  end

  def self.find_package(price)
    Package.main.each do |package|
      return package if package.price_range.include?(price.to_i)
    end
  end

  def formatted
    "#{name} - #{price_text}"
  end
end
