# Generated by Django 3.2.9 on 2022-01-09 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_alter_erauser_email'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immatriculation', models.CharField(max_length=10, unique=True)),
                ('weight', models.IntegerField()),
                ('passengers_seat', models.SmallIntegerField()),
                ('construction', models.DateField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='AircraftComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=200)),
                ('serial_number', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='AircraftLicence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_type', models.CharField(choices=[('A', 'Airplane'), ('H', 'Helicopter'), ('S', 'Sailplane'), ('B', 'Balloon'), ('U', 'Unknown')], max_length=5)),
                ('commercial', models.BooleanField(default=False)),
                ('night', models.BooleanField(default=False)),
                ('instructor', models.BooleanField(default=False)),
                ('delivery_date', models.DateField()),
                ('check_flight_date', models.DateField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='AircraftManufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.erauser')),
            ],
        ),
        migrations.CreateModel(
            name='BalloonLicence',
            fields=[
                ('aircraftlicence_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraftlicence')),
                ('class_type', models.CharField(choices=[('GB', 'Generic Balloon'), ('GHAB', 'Generic Hot-Air Balloon'), ('AHAB', 'Hot-Air Balloon, class A'), ('BHAB', 'Hot-Air Balloon, class B'), ('CHAB', 'Hot-Air Balloon, class C'), ('DHAB', 'Hot-Air Balloon, class D'), ('GGB', 'Generic Gas Balloon'), ('GMB', 'Generic Mixed Balloon'), ('GHAAB', 'Generic Hot-Air Airship'), ('UB', 'Unknown Balloon')], max_length=5)),
                ('licence_specific_type', models.CharField(choices=[('GLB', 'Generic Balloon licence'), ('GHAB', 'Generic Hot-Air Balloon'), ('BPL', 'European balloon pilot licence'), ('ULB', 'Unknown Balloon licence')], max_length=5)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraftlicence',),
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('aircraftcomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraftcomponent')),
                ('mounting_point', models.CharField(choices=[('4', '4 mounting points'), ('8', '8 mounting points'), ('G', 'Gas type')], max_length=1)),
                ('weight', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraftcomponent',),
        ),
        migrations.CreateModel(
            name='Burner',
            fields=[
                ('aircraftcomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraftcomponent')),
                ('weight', models.SmallIntegerField()),
                ('burner_type', models.SmallIntegerField(choices=[(1, 'Single'), (2, 'Double'), (3, 'Triple'), (4, 'Quadra')])),
                ('gas_connection_type', models.CharField(choices=[('R', 'Rego'), ('T', 'Tema')], max_length=1)),
                ('liquid_pilot_light', models.BooleanField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraftcomponent',),
        ),
        migrations.CreateModel(
            name='Envelope',
            fields=[
                ('aircraftcomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraftcomponent')),
                ('weight', models.SmallIntegerField()),
                ('enveloppe_size', models.SmallIntegerField()),
                ('cubic_meter_size', models.BooleanField(default=True)),
                ('mounting_point', models.CharField(choices=[('4', '4 mounting points'), ('8', '8 mounting points'), ('G', 'Gas type')], max_length=1)),
                ('description', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraftcomponent',),
        ),
        migrations.CreateModel(
            name='FuelCylinder',
            fields=[
                ('aircraftcomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraftcomponent')),
                ('capacity', models.SmallIntegerField()),
                ('gas_connection_type', models.CharField(choices=[('R', 'Rego'), ('T', 'Tema')], max_length=1)),
                ('liquid_connection', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraftcomponent',),
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_type', models.CharField(choices=[('1', 'Class 1'), ('2', 'Class 2'), ('L', 'LAPL')], max_length=1)),
                ('delivery_date', models.DateField()),
                ('expiration_date', models.DateField(blank=True)),
                ('pilot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_log.pilot')),
            ],
        ),
        migrations.CreateModel(
            name='FlightBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pilot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_log.pilot')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_flight_log.flightbook_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=500, null=True)),
                ('take_off_time', models.DateTimeField()),
                ('take_off_place', models.CharField(max_length=250)),
                ('landing_time', models.DateTimeField()),
                ('landing_place', models.CharField(max_length=250)),
                ('nb_landing', models.SmallIntegerField(default=1)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.aircraft')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_log.flightbook')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_flight_log.flight_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='AircraftModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_type', models.CharField(choices=[('A', 'Airplane'), ('H', 'Helicopter'), ('S', 'Sailplane'), ('B', 'Balloon'), ('U', 'Unknown')], max_length=1)),
                ('aircraft_specific_type', models.CharField(blank=True, max_length=5)),
                ('model', models.CharField(max_length=200, unique=True)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.aircraftmanufacturer')),
            ],
        ),
        migrations.AddField(
            model_name='aircraftlicence',
            name='pilot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_log.pilot'),
        ),
        migrations.AddField(
            model_name='aircraftlicence',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_flight_log.aircraftlicence_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='aircraftcomponent',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.aircraftmanufacturer'),
        ),
        migrations.AddField(
            model_name='aircraftcomponent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_flight_log.aircraftcomponent_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.aircraftmodel'),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_flight_log.aircraft_set+', to='contenttypes.contenttype'),
        ),
        migrations.CreateModel(
            name='Balloon',
            fields=[
                ('aircraft_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.aircraft')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.basket')),
                ('envelope', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.envelope')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.aircraft',),
        ),
        migrations.CreateModel(
            name='HotAirBalloon',
            fields=[
                ('balloon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flight_log.balloon')),
                ('burner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flight_log.burner')),
                ('fuel_cylinders', models.ManyToManyField(to='flight_log.FuelCylinder')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('flight_log.balloon',),
        ),
    ]
