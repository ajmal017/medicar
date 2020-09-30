from rest_framework import serializers
from .models import (
    Specialty, Doctor, Agenda, MedicalAppointment
)


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    specialty = serializers.SerializerMethodField()

    def get_specialty(self, obj):
        return SpecialtySerializer(Specialty.objects.filter(
            doctor=obj).first(), read_only=True).data

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'crm',
            'email',
            'phone',
            'specialty'
        ]


class AgendaSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    def get_doctor(self, obj):
        return DoctorSerializer(Doctor.objects.filter(
            id=obj.doctor.id).first(), read_only=True).data

    class Meta:
        model = Agenda
        fields = [
            'id',
            'day',
            'schedule',
            'doctor',
        ]


class MedicalAppointmentSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    def get_day(self, obj):
        return obj.agenda.get_day()

    def get_doctor(self, obj):
        return DoctorSerializer(Doctor.objects.filter(
            id=obj.agenda.doctor_id).first(), read_only=True).data

    class Meta:
        model = MedicalAppointment
        fields = [
            'id',
            'day',
            'hourly',
            'scheduling_date',
            'doctor',
        ]
