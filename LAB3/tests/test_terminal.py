"""Extended tests for Terminal, Gate, and BoardingPass models."""
import pytest

from airport_system.domain.terminal import Gate, Terminal, BoardingPass
from airport_system.domain.enums import SecurityLevel


class TestGate:
    """Tests for Gate class."""

    def test_gate_basic(self):
        """Test basic Gate creation."""
        gate = Gate(
            gate_id="G1",
            terminal_code="T1"
        )
        assert gate.gate_id == "G1"
        assert gate.terminal_code == "T1"
        assert gate.is_open is True
        assert gate.current_flight_id is None

    def test_gate_assign_flight(self):
        """Test assigning flight to gate."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        gate.assign_flight("FL123")
        assert gate.current_flight_id == "FL123"

    def test_gate_clear_flight(self):
        """Test clearing flight from gate."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        gate.assign_flight("FL123")
        gate.clear_flight()
        assert gate.current_flight_id is None

    def test_gate_close(self):
        """Test closing gate."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        gate.close()
        assert gate.is_open is False

    def test_gate_open(self):
        """Test opening gate."""
        gate = Gate(gate_id="G1", terminal_code="T1", is_open=False)
        gate.open()
        assert gate.is_open is True

    def test_gate_is_free_true(self):
        """Test is_free when gate is open and no flight."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        assert gate.is_free() is True

    def test_gate_is_free_false_has_flight(self):
        """Test is_free when gate has assigned flight."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        gate.assign_flight("FL123")
        assert gate.is_free() is False

    def test_gate_is_free_false_closed(self):
        """Test is_free when gate is closed."""
        gate = Gate(gate_id="G1", terminal_code="T1")
        gate.close()
        assert gate.is_free() is False


class TestTerminal:
    """Tests for Terminal class."""

    def test_terminal_basic(self):
        """Test basic Terminal creation."""
        terminal = Terminal(
            code="T1",
            name="Terminal 1",
            security_level=SecurityLevel.PUBLIC
        )
        assert terminal.code == "T1"
        assert terminal.name == "Terminal 1"
        assert terminal.gates == []

    def test_terminal_add_gate(self):
        """Test adding gate to terminal."""
        terminal = Terminal(code="T1")
        gate = Gate(gate_id="G1", terminal_code="T1")
        terminal.add_gate(gate)
        assert len(terminal.gates) == 1
        assert terminal.gates[0] is gate

    def test_terminal_find_free_gate_exists(self):
        """Test finding free gate when one exists."""
        gate1 = Gate(gate_id="G1", terminal_code="T1")
        gate2 = Gate(gate_id="G2", terminal_code="T1")
        gate1.assign_flight("FL123")
        terminal = Terminal(code="T1", gates=[gate1, gate2])
        free = terminal.find_free_gate()
        assert free is gate2

    def test_terminal_find_free_gate_none(self):
        """Test finding free gate when none exists."""
        gate1 = Gate(gate_id="G1", terminal_code="T1")
        gate1.assign_flight("FL123")
        terminal = Terminal(code="T1", gates=[gate1])
        free = terminal.find_free_gate()
        assert free is None

    def test_terminal_find_free_gate_empty(self):
        """Test finding free gate when no gates."""
        terminal = Terminal(code="T1")
        free = terminal.find_free_gate()
        assert free is None

    def test_terminal_is_international_true(self):
        """Test is_international when has international gate."""
        gate1 = Gate(gate_id="G1", terminal_code="T1", supports_international=False)
        gate2 = Gate(gate_id="G2", terminal_code="T1", supports_international=True)
        terminal = Terminal(code="T1", gates=[gate1, gate2])
        assert terminal.is_international_terminal() is True

    def test_terminal_is_international_false(self):
        """Test is_international when no international gates."""
        gate1 = Gate(gate_id="G1", terminal_code="T1", supports_international=False)
        gate2 = Gate(gate_id="G2", terminal_code="T1", supports_international=False)
        terminal = Terminal(code="T1", gates=[gate1, gate2])
        assert terminal.is_international_terminal() is False

    def test_terminal_is_international_empty(self):
        """Test is_international when no gates."""
        terminal = Terminal(code="T1")
        assert terminal.is_international_terminal() is False

    def test_terminal_available_gates_count(self):
        """Test counting available gates."""
        gate1 = Gate(gate_id="G1", terminal_code="T1")
        gate2 = Gate(gate_id="G2", terminal_code="T1")
        gate3 = Gate(gate_id="G3", terminal_code="T1")
        gate1.assign_flight("FL123")
        terminal = Terminal(code="T1", gates=[gate1, gate2, gate3])
        assert terminal.available_gates_count() == 2


class TestBoardingPass:
    """Tests for BoardingPass class."""

    def test_boarding_pass_basic(self):
        """Test basic BoardingPass creation."""
        bp = BoardingPass(
            boarding_pass_id="BP1",
            booking_id="BKG1",
            passenger_name="John Doe",
            gate_id="G1",
            seat_number="1A"
        )
        assert bp.boarding_pass_id == "BP1"
        assert bp.booking_id == "BKG1"
        assert bp.passenger_name == "John Doe"
        assert bp.gate_id == "G1"
        assert bp.seat_number == "1A"

    def test_boarding_pass_change_gate(self):
        """Test changing gate on boarding pass."""
        bp = BoardingPass(
            boarding_pass_id="BP1",
            booking_id="BKG1",
            passenger_name="John Doe",
            gate_id="G1",
            seat_number="1A"
        )
        bp.change_gate("G5")
        assert bp.gate_id == "G5"
