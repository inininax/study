const printLabel = (obj: { label: string }): void => {
    console.log(obj.label);
};

let myObj = {label: 'Size 10 Object', size: 10};
printLabel(myObj);

// ---
interface LabeledValue {
    label: string
}

const printLabeledValue = (obj: LabeledValue): void => {
    console.log(obj.label)
}

printLabeledValue(myObj);