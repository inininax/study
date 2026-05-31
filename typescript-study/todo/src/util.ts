export function getIsValidEnumValue(enumObject: any, value: number | string) {
  return Object.keys(enumObject)
    .filter(key => isNaN(Number(key))) // Not-A-Number(
    .some(key => enumObject[key] === value);
}
