"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get('designation', '')
        assert isinstance(self.designation, str)        
        self.name = info.get('name')
        if not info['diameter']:
            self.diameter = float('nan')
        else:
            self.diameter = float(info['diameter'])
        assert isinstance(self.diameter, float)
        hazardous_outputs = {'N': False, 'Y': True, False: False, '': False}
        input_hazard = info.get('hazardous', False)
        self.hazardous = hazardous_outputs[input_hazard]
        assert isinstance(self.hazardous, bool)
        self.approaches = info.get('approaches', [])

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name != '':
            return f'{self.designation} ({self.name})'
        return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous == False:
            return (f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and "
                    f"is not potentially hazardous.")
        return (f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and is "
                f"potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")
        
    def serialize(self):
        """Return a dictionary of `NearEarthObject` attributes."""
        return {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, time: datetime, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        :time: datetime keyword argument
        """        
        self._designation = info.get('designation', '')
        assert isinstance(self._designation, str)
        self.time = cd_to_datetime(time)  
        assert isinstance(self.time, datetime.datetime)    
        self.distance = float(info.get('distance', 0.0))
        assert isinstance(self.distance, float)
        self.velocity = float(info.get('velocity', 0.0))
        assert isinstance(self.velocity, float)
        self.neo = info.get('neo', None)
                                       
    @property
    def designation(self):
        """Return the designation attribute."""
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """        
        return datetime_to_str(self.time)
    
    @property
    def fullname(self):
        """Return a representation of the full name of this CloseApproach."""
        if self.name != '':
            return f'{self._designation} ({self.name})'
        return f'{self._designation}'

    def __str__(self):
        """Return `str(self)`."""
        return (f"At {self.time_str}, '{self.neo.fullname}' approaches Earth, at a distance "
                f"of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s.")
    
    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
        
    def serialize(self):
        """Return a dictionary of `CloseApproach` attributes."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity
        }
