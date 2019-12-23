from pathlib import Path
from typing import Iterator, List

from processor import Processor, ProgramHalt


class D23Processor(Processor):
    def run_network_generator(self, nid: int, output_batch: int) -> Iterator[List[int]]:
        ip = 0
        self.input.append(nid)
        try:
            while True:
                if self.memory[ip] % 10 == 3:  # If next instruction is input...
                    yield
                    if not self.input:
                        self.input.append(-1)

                ip = self.func_by_instruction_pointer(ip)

                if len(self.output) == output_batch:
                    yield self.output
                    self.output.clear()
        except ProgramHalt:
            raise NotImplementedError(f"Don't expect the bot to ever halt the program")


def run_network(program, num_comps: int = 50, part_2=False) -> int:
    machines = [D23Processor(program) for _ in range(num_comps)]
    processors = [bot.run_network_generator(n, 3) for n, bot in enumerate(machines)]
    [next(proc) for proc in processors]  # Move to first yield to accept .send()
    nat_y_last = nat_y = nat_x = None
    idle_check = 0
    while True:
        any_output = False
        for i in range(num_comps):
            output = next(processors[i])

            if output is not None:
                any_output = True
                address, x, y = output
                if 0 <= address < num_comps:
                    machines[address].input += [x, y]
                elif address == 255:
                    if part_2:
                        nat_x, nat_y = x, y
                    else:
                        return y
                else:
                    raise ValueError(f"Unknown output {output} from proc {i}")

        if not any_output and all(not m.input for m in machines):
            idle_check += 1
            if idle_check >= 2:
                idle_check = 0
                assert not (nat_x is nat_y is None)

                machines[0].input += [nat_x, nat_y]
                if nat_y == nat_y_last:
                    return nat_y
                else:
                    nat_y_last = nat_y


if __name__ == "__main__":
    DATA = Path("day23.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(run_network(int_list))
    print(run_network(int_list, part_2=True))
