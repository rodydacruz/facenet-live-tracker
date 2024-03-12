from lib.people_service import PersonCRUD

# Example usage:
crud = PersonCRUD('persons.db')

# Create a person with photo URL
person_id = crud.create_person('Rody', 30, 'rodylag@example.com', 'https://sniacapps.gov.cv/sniac_prod/SNIAC.IGRP_PORTAL.download_file_img_bio?p_tipo_doc=1&p_id_pessoa=1999050303795&p_id_tp_imagem=1')

# Get a person
person = crud.get_person(person_id)
print("Retrieved Person:", person)

# Get all persons
all_persons = crud.get_all_persons()
print("All Persons:", all_persons)

# Delete a person
# crud.delete_person(person_id)