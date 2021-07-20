# Versions

- Ruby 3.0.1
- Bundler 2.2.24
- Ruby on Rails 6.1.4
- MySQL 8.0.25

### Demo Template

https://elements.envato.com/quote-quotation-or-survey-form-wizard-JPMK24

### Requirement

Stage 1 Questions:
1) What type of Loss? <type dropdown>
a. Options: Fire, Wind/Hail, Water, Frozen Pipe, Collapse, Car into a dwelling, Fence, (Other => text input), Named Storm (text input appears)
2) Date of Loss
a. Datepicker
3) Property Type <radio>
a. Single family, Multifamily, Condo, Commercial, Mix-use, other structure
i. IF apartment/multifamily(additional dropdown appears with question “Were other units effected?” <radio yes/no> <====> "Other units effected" only shows up on condo, multifamily and commercial
3
4) Location of Loss (Google map api) <text>
5) Declarations Page(or upload policy page)<file upload> -> before it was Policy Limit
6) Insurance Estimate <file upload>
7) Was there damage outside of what your insurance company reported? (Radio yes/no IF Yes <text field>

Stage 2
1) First Name, Last Name, Address, City, State, Zipcode, Phone, Email, Contact preference (<radio email/phone>)
2) Packgace
the last 3 services are additional addons so mutiselect with them should be available
- 1-$1,000 $39.99
- $1,000-$2,500 $49.99
- $2,500-$5,000 $59.99
- $5,000-$15,000 $69.99
- $15,000-$30,000 $79.99
- $30,000-$50,000 $89.99
- Sumplemental Claim $199.99
- 20 Min Consultation $129.99
- Will Refer a Qualified Public Adjuster In your Area FREE

if there is extra damage, we will ask them to pay for supplemental room

If they click yes, we need to add "Room Name", "Room dimensions (L x W x H) and the abilit yto add more than one room

Ok - also if on stage 1 "Is there room is missing" then on stage 2 they have the option for "supplemental claim" if this is not checked we will omit it
