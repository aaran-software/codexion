import { useState } from 'react';
import fieldConfig from "../../../../../public/JSON/GrandStream/table.json";
import table_data from "../../../../../public/JSON/GrandStream/grandstream.json";
import type { ApiList, Field } from '../../../../Components/common/commonform';
import FormLayout from '../../../../Components/common/FormLayout';

function GrandStream() {
  const fieldSection = fieldConfig.grandstream.calllog;

  // ✅ Extract all fields
  const allFields = Object.values(fieldSection)
    .flatMap((section: any) => section.fields);

  // ✅ Map fields by key
  const fieldMap: Record<string, any> = allFields.reduce((acc, field) => {
    acc[field.key] = field;
    return acc;
  }, {});

  // ✅ Headers to show in the table
  const head = allFields.filter((field) => field.inTable);

  // ✅ Flatten all call logs
  const data = (table_data.response?.cdr_root ?? []).map((cdrItem: any, index: number) => {
    const flat: Record<string, any> = {
      id: cdrItem.main_cdr?.AcctId || `cdr-${index}`,
      cdr: cdrItem.cdr,
    };

    Object.entries(cdrItem).forEach(([sectionKey, sectionVal]) => {
      if (typeof sectionVal === 'object' && sectionVal !== null) {
        Object.entries(sectionVal).forEach(([key, val]) => {
          flat[key] = val;
        });
      } else {
        flat[sectionKey] = sectionVal;
      }
    });

    return flat;
  });

  // ✅ Build grouped field layout
  const groupedFields = (table_data.response?.cdr_root ?? []).flatMap((cdrItem: any) => {
    return Object.entries(cdrItem)
      .filter(([key]) => key !== 'cdr')
      .map(([sectionKey, sectionData]) => {
        const fields = typeof sectionData === 'object' && sectionData !== null
          ? Object.entries(sectionData).map(([key]) => {
              const field = fieldMap[key] || {
                key,
                label: key,
                type: 'textinput',
              };
              return {
                id: key,
                label: field.label || key,
                type: field.type as Field["type"],
                className: 'w-full',
                errMsg: `Enter ${field.label || key}`,
                ...(field.type?.includes('dropdown') && field.options
                  ? { options: field.options }
                  : {}),
                readApi: field.readApi,
                updateApi: field.updateApi,
                apiKey: field.apiKey,
                createKey: field.createKey,
              };
            })
          : [];

        return {
          title: `${sectionKey.replace(/_/g, ' ').toUpperCase()} (${cdrItem.cdr})`,
          sectionKey,
          fields,
        };
      });
  });

  // ✅ Fields for printing
  const printableFields = allFields.filter((field) => field.isPrint);

  const [formApi] = useState<ApiList>({
    create: "/api/resource/Customer",
    read: "/api/resource/Customer",
    update: "/api/resource/Customer",
    delete: "/api/resource/Customer",
  });

  return (
    <div>
      <FormLayout
        groupedFields={groupedFields}
        head={head}
        formApi={formApi}
        printableFields={printableFields}
        data={data}
      />
    </div>
  );
}

export default GrandStream;
