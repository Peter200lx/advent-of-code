from pathlib import Path

from processor import Processor, ProgramHalt


class D23Processor(Processor):
    def run_network_generator(self, nid, output_batch):
        ip = 0
        self.input.append(nid)
        try:
            while True:
                if self.memory[ip] % 10 == 3:  # If next instruction is input...
                    yield
                    if not self.input:
                        self.input.append((-1))

                ip = self.func_by_instruction_pointer(ip)

                if len(self.output) == output_batch:
                    yield self.output
                    self.output.clear()
        except ProgramHalt:
            raise NotImplementedError(f"Don't expect the bot to ever halt the program")


def run_network(program, num_comps: int, part_1=True) -> int:
    machines = [D23Processor(program) for _ in range(num_comps)]
    processors = [bot.run_network_generator(n, 3) for n, bot in enumerate(machines)]
    [next(proc) for proc in processors]  # Move to first yield to accept .send()
    nat_y_last = None
    idle_check = 0
    try:
        while True:
            any_output = False
            for i in range(num_comps):
                output = next(processors[i])
                if output is not None:
                    any_output = True
                    address, X, Y = output
                    if address == 255:
                        if part_1:
                            return Y
                        else:
                            natX, natY = X, Y
                    else:
                        machines[address].input += [X, Y]

            if not any_output and all(len(m.input) <= 1 for m in machines):
                idle_check += 1
                if idle_check > 2:
                    idle_check = 0
                    machines[0].input += [natX, natY]
                    if natY == nat_y_last:
                        return natY
                    else:
                        nat_y_last = natY

    except StopIteration:
        raise NotImplementedError(f"Don't expect the bot to ever halt the program")


if __name__ == "__main__":
    DATA = Path("day23.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(run_network(int_list, 50))
    print(run_network(int_list, 50, part_1=False))
