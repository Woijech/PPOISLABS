"""Tests for Employee, Pilot, CabinCrew, and GroundStaff domain models."""
import pytest

from airport_system.domain.employee import Employee, Pilot, CabinCrew, GroundStaff
from airport_system.domain.enums import EmployeeRole


def test_employee_basic_operations():
    """Test basic Employee operations."""
    emp = Employee(
        employee_id="E1",
        name="John Doe",
        role=EmployeeRole.GROUND_STAFF,
        username="jdoe"
    )
    assert emp.is_active_staff() is True
    emp.deactivate()
    assert emp.active is False
    assert emp.is_active_staff() is False
    emp.activate()
    assert emp.active is True


def test_employee_password():
    """Test Employee password management."""
    emp = Employee(employee_id="E1", name="Jane", role=EmployeeRole.GROUND_STAFF)
    emp.set_password("secure123")
    assert emp.verify_password("secure123") is True
    assert emp.verify_password("wrong") is False


def test_employee_high_security_access():
    """Test high security access check."""
    pilot = Employee(employee_id="E1", name="Pilot", role=EmployeeRole.PILOT)
    security = Employee(employee_id="E2", name="Security", role=EmployeeRole.SECURITY)
    cabin = Employee(employee_id="E3", name="Cabin", role=EmployeeRole.CABIN_CREW)
    ground = Employee(employee_id="E4", name="Ground", role=EmployeeRole.GROUND_STAFF)

    assert pilot.can_access_high_security() is True
    assert security.can_access_high_security() is True
    assert cabin.can_access_high_security() is False
    assert ground.can_access_high_security() is False


def test_pilot_operations():
    """Test Pilot specific operations."""
    pilot = Pilot(
        employee_id="P1",
        name="Captain Smith",
        role=EmployeeRole.PILOT,
        license_number="LIC123",
        flight_hours=100
    )
    assert pilot.flight_hours == 100
    pilot.add_flight_hours(50)
    assert pilot.flight_hours == 150


def test_pilot_invalid_hours():
    """Test adding zero or negative flight hours raises error."""
    pilot = Pilot(
        employee_id="P1",
        name="Captain Smith",
        role=EmployeeRole.PILOT,
        license_number="LIC123",
        flight_hours=100
    )
    with pytest.raises(ValueError, match="Hours must be positive"):
        pilot.add_flight_hours(0)
    with pytest.raises(ValueError, match="Hours must be positive"):
        pilot.add_flight_hours(-10)


def test_cabin_crew_operations():
    """Test CabinCrew specific operations."""
    crew = CabinCrew(
        employee_id="C1",
        name="Jane",
        role=EmployeeRole.CABIN_CREW,
        languages_spoken=3
    )
    assert crew.can_serve_language(2) is True
    assert crew.can_serve_language(3) is True
    assert crew.can_serve_language(4) is False


def test_ground_staff_operations():
    """Test GroundStaff specific operations."""
    staff = GroundStaff(
        employee_id="G1",
        name="Bob",
        role=EmployeeRole.GROUND_STAFF
    )
    assert staff.is_assigned() is False
    staff.assign_station("Terminal A")
    assert staff.is_assigned() is True
    assert staff.station == "Terminal A"
