"""
Models for just our tests
"""
from django.db import models as dmodels

from opal.core import fields
from opal import models
from opal.core import lookuplists


class Birthday(models.PatientSubrecord):
    birth_date = dmodels.DateField(blank=True)
    party = dmodels.DateTimeField(blank=True, null=True)


class Hat(lookuplists.LookupList):
    pass


class HatWearer(models.EpisodeSubrecord):
    _sort = 'name'
    _title = 'Wearer of Hats'

    name = dmodels.CharField(max_length=200)
    hats = dmodels.ManyToManyField(Hat, related_name="hat_wearers")
    wearing_a_hat = dmodels.BooleanField(default=True)


class InvisibleHatWearer(models.EpisodeSubrecord):
    BULK_SERIALISE = False
    name = dmodels.CharField(max_length=200)
    wearing_a_hat = dmodels.BooleanField(default=True)


class HouseOwner(models.PatientSubrecord):
    pass


class House(dmodels.Model):
    address = dmodels.CharField(max_length=200)
    house_owner = dmodels.ForeignKey(HouseOwner, null=True, blank=True)


class Dog(lookuplists.LookupList):
    pass


class DogOwner(models.EpisodeSubrecord):
    name = dmodels.CharField(max_length=200, default="Catherine")
    dog = fields.ForeignKeyOrFreeText(Dog, default="spaniel")
    least_favourite_dog = fields.ForeignKeyOrFreeText(Dog, related_name='hated_dogs')
    ownership_start_date = dmodels.DateField(blank=True, null=True, verbose_name="OSD")


class HoundOwner(models.EpisodeSubrecord):
    name = dmodels.CharField(max_length=200, default=lambda: "Philipa")
    dog = fields.ForeignKeyOrFreeText(Dog, verbose_name="hound", default=lambda: "spaniel")


class FavouriteDogs(models.PatientSubrecord):
    dogs = dmodels.ManyToManyField(Dog, related_name='favourite_dogs')


class InvisibleDog(models.PatientSubrecord):
    BULK_SERIALISE = False
    name = dmodels.CharField(max_length=200, default="Catherine")


class Colour(models.EpisodeSubrecord):
    _clonable = False
    _advanced_searchable = False
    _exclude_from_extract = True
    _angular_service = 'Colour'
    _icon = "fa fa-comments"

    name = dmodels.CharField(max_length=200)


class PatientColour(models.PatientSubrecord):
    name = dmodels.CharField(max_length=200)
    _exclude_from_extract = True


class FamousLastWords(models.PatientSubrecord):
    _is_singleton = True
    _read_only = True

    words = dmodels.CharField(verbose_name="only words", max_length=200, blank=True, null=True)


class EpisodeName(models.EpisodeSubrecord):
    _is_singleton = True

    name = dmodels.CharField(max_length=200, blank=True, null=True)


COLOUR_CHOICES = (
    ('purple', 'purple'),
    ('yellow', 'yellow'),
    ('blue', 'blue'),
)


class FavouriteColour(models.PatientSubrecord):
    _is_singleton = True
    name = dmodels.CharField(
        max_length=200, blank=True, null=True, choices=COLOUR_CHOICES
    )


class ExternalSubRecord(
    models.EpisodeSubrecord,
    models.ExternallySourcedModel,
):
    name = dmodels.CharField(max_length=200, blank=True, null=True)

# We shouldn't, but we basically insist on some non-core models being there.
if not getattr(models.Patient, 'demographics_set', None):

    class Demographics(models.PatientSubrecord):
        _is_singleton = True

        hospital_number = dmodels.CharField(max_length=200, blank=True, null=True)
        nhs_number = dmodels.CharField(max_length=200, blank=True, null=True)
        first_name = dmodels.CharField(max_length=200, blank=True, null=True)
        surname = dmodels.CharField(max_length=200, blank=True, null=True)
        date_of_birth = dmodels.DateField(blank=True, null=True)
        sex = fields.ForeignKeyOrFreeText(models.Gender)
        birth_place = fields.ForeignKeyOrFreeText(models.Destination)
        death_indicator = dmodels.BooleanField(default=False)

        pid_fields = 'first_name', 'surname',

if not getattr(models.Episode, 'location_set', None):

    class Location(models.EpisodeSubrecord):
        _is_singleton = True

        ward = dmodels.CharField(max_length=200, blank=True, null=True)
        bed = dmodels.CharField(max_length=200, blank=True, null=True)



if not getattr(models.Episode, 'symptoms', None):
    class SymptomComplex(models.SymptomComplex):
        pass

if not getattr(models.Episode, 'patientconsultation_set', None):
    class PatientConsultation(models.PatientConsultation):
        pass
