import RadioGroup, { type RadioOption } from "../../../../../resources/components/radioGroup/radio_group";

const genderOptions: RadioOption[] = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female"},
  { value: "other", label: "Other"},
];

const htmlOptions: RadioOption[] = [
  {
    value: "a",
    label: "Hyper Text Markup Language",
    description: "Standard language for creating web pages.",
  },
  {
    value: "b",
    label: "Home Tool Markup Language",
    description: "Common misinterpretation of HTML.",
  },
  {
    value: "c",
    label: "Hyperlinks and Text Markup Language",
    description: "Sounds correct, but it's not official.",
  },
];

export default function RadioGroupComponent() {
  return (
    <div className="p-6 space-y-8 w-[70%] block m-auto">
      <fieldset className="space-y-4 border border-gray-200 rounded-md p-4">
        <legend className="text-lg font-semibold px-1">Select Gender</legend>
        <RadioGroup
          name="gender"
          options={genderOptions}
          defaultValue="male"
          onChange={(val) => console.log("Gender:", val)}
        />
      </fieldset>

      {/* HTML Question Group */}
      <fieldset className="space-y-4 border border-gray-200 rounded-md p-4">
        <legend className="text-lg font-semibold px-1">What does HTML stand for?</legend>
        <RadioGroup
          name="html"
          options={htmlOptions}
          onChange={(val) => console.log("HTML Answer:", val)}
        />
      </fieldset>
    </div>
  );
}
