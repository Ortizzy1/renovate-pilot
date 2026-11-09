import semver from "semver";

/** True when `version` satisfies the semver `range`. */
export function isCompatible(version, range) {
  return semver.satisfies(version, range);
}

/** Highest valid version in the list, or null. */
export function newest(versions) {
  const valid = versions.filter((v) => semver.valid(v));
  return valid.length ? valid.sort(semver.rcompare)[0] : null;
}
