from src.errors.company_exeptions import InvalidCompanyNameError, InvalidCompanyEmailError, InvalidCompanyWebsiteError, InvalidCompanyPhoneError, InvalidBusinessTypeError
from email_validator import validate_email
from urllib.parse import urlparse

class Company:

    VALID_BUSINESS_TYPES = {
        "MANUFACTURER",
        "DISTRIBUTOR",
        "SERVICE PROVIDER"
    }

    def __init__(self, name, description, website, email, phone, address, business_type):
        self.name = self.validate_name_company(name)
        self.description = description
        self.website = self.validate_website_company(website)
        self.email = email
        self.phone = self.validate_phone_company(phone)
        self.address = address
        self.business_type = business_type

    def validate_name_company(self, name):
        if not name or len(name) < 2:
           raise InvalidCompanyNameError("O nome da empresa deve possuir pelo menos 2 caracteres.")
        return name

    def validate_email_company(self, email):
        try:
            valid = validate_email(email)
            return email
        except:
            raise InvalidCompanyEmailError(f'E-mail Inválido: {email}')

    def validate_website_company(self, website):
        parsed = urlparse(website)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise InvalidCompanyWebsiteError(f"Website inválido: {website}.")
        return website


    def validate_phone_company(self, phone):
        if not phone or len(phone.strip()) < 8:
            raise InvalidCompanyPhoneError(f"Telefone inválido. {phone}")
        return phone


    def validate_business_company(self, business_type):
        if business_type not in self.VALID_BUSINESS_TYPES:
            raise InvalidBusinessTypeError(f"Tipo de negócio inválido.: {business_type}")
        return business_type



def biuld_company(name, description, website, email, phone, address, business_type) -> Company:
    company = Company(name, description, website, email, phone, address, business_type)

    return company
