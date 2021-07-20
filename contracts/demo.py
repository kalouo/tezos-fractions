import smartpy as sp

# A typical SmartPy program has the following form:

# A class of contracts
class MyContract(sp.Contract):
    def __init__(self, x, y):
        self.init(x = x,
                  y = y)

    # An entry point, i.e., a message receiver
    # (contracts react to messages)
    @sp.entry_point
    def myEntryPoint(self, params):
        sp.verify(self.data.x <= 123)
        self.data.x += params

# Tests
@sp.add_test(name = "Welcome")
def test():
    # We define a test scenario, together with some outputs and checks
    scenario = sp.test_scenario()

    # We first define a contract and add it to the scenario
    c1 = MyContract(12, 123)
    scenario += c1

    # And call some of its entry points
    scenario += c1.myEntryPoint(12)
    scenario += c1.myEntryPoint(13)
    scenario += c1.myEntryPoint(14)
    scenario += c1.myEntryPoint(50)
    scenario += c1.myEntryPoint(50)
    scenario += c1.myEntryPoint(50).run(valid = False) # this is expected to fail

    # Finally, we check its final storage
    scenario.verify(c1.data.x == 151)

    # We can define another contract using the current state of c1
    c2 = MyContract(1, c1.data.x)
    scenario += c2
    scenario.verify(c2.data.y == 151)

sp.add_compilation_target("demo", MyContract(0, 0))