import { Calendar22 } from '../../../../../resources/components/calendar-22';
import { Calendar } from '../../../../../resources/components/calendar';
import { useState } from 'react';
import { DatePicker } from '../../../../../resources/components/datepicker/DatePicker';

function CalendarComponents() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined);
  const [selected, setSelected] = useState<Date | undefined>();
  const [datePickerSelectedDate, setDatePickerSelectedDate] = useState<Date | undefined>(new Date());

  return (
    <div className="p-4 flex flex-row flex-wrap gap-10">
      {/* Calendar22 */}
      <div>
        <Calendar22
          id="birth-date"
          value={selectedDate}
          onChange={setSelectedDate}
          label="Select a date"
          err={!selectedDate ? "" : ""}
          className="max-w-xs"
        />
        {selectedDate && (
          <p className="mt-4 text-sm text-foreground">
            Selected: {selectedDate.toLocaleDateString()}
          </p>
        )}
      </div>

      {/* Calendar */}
      <div className="flex flex-col">
        <Calendar
          mode="single"
          selected={selected}
          onSelect={setSelected}
          captionLayout="dropdown"
          className="bg-white border rounded-md p-4"
        />
        {selected && (
          <p className="mt-4 text-sm text-foreground">
            Selected: {selected.toLocaleDateString()}
          </p>
        )}
      </div>

      {/* DatePicker */}
      <div className="flex flex-col">
        <DatePicker
          model={datePickerSelectedDate}
          formatStr="MMM dd, yyyy"
          onChange={(date) => setDatePickerSelectedDate(date)}
        />
        {datePickerSelectedDate && (
          <p className="mt-4 text-sm text-foreground">
            Selected: {datePickerSelectedDate.toLocaleDateString()}
          </p>
        )}
      </div>
    </div>
  );
}

export default CalendarComponents;
