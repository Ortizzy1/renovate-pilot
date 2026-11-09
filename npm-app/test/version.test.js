import { test } from "node:test";
import assert from "node:assert/strict";
import { isCompatible, newest } from "../src/version.js";

test("isCompatible accepts versions inside the range", () => {
  assert.equal(isCompatible("1.4.2", "^1.2.0"), true);
});

test("isCompatible rejects versions outside the range", () => {
  assert.equal(isCompatible("2.0.0", "^1.2.0"), false);
});

test("newest picks the highest valid version and ignores junk", () => {
  assert.equal(newest(["1.0.0", "not-a-version", "1.10.0", "1.9.9"]), "1.10.0");
  assert.equal(newest([]), null);
});
