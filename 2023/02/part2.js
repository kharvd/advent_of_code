const fs = require("node:fs");
const memory = new WebAssembly.Memory({ initial: 1 });

const importObject = {
  js: {
    mem: memory,
  },
};

const data = new Uint8Array(memory.buffer);
// console.log("123".split("").map((c) => c.charCodeAt(0)));
// const str = `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
// Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
// Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
// Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
// Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
// `;
const str = fs.readFileSync("./input.txt", "utf8");
data.set(
  str.split("").map((c) => c.charCodeAt(0)),
  0
);
data[str.length] = 0;

const wasmBuffer = fs.readFileSync("./part2.wasm");
WebAssembly.instantiate(wasmBuffer, importObject).then((wasmModule) => {
  const { main } = wasmModule.instance.exports;
  const result = main(str.length);
  console.log(result);
});
