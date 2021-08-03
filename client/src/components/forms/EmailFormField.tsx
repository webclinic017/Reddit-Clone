import React from 'react';
import { FormControl, FormLabel, Input } from '@chakra-ui/react';

interface EmailFormFieldProps {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FormEvent) => void;
}

function EmailFormField({
  label,
  value,
  onChange,
  onBlur,
}: EmailFormFieldProps) {
  return (
    <FormControl className="formControl">
      <FormLabel>{label}</FormLabel>
      <Input
        type="email"
        placeholder="email"
        value={value}
        onChange={onChange}
        onBlur={onBlur}
      />
    </FormControl>
  );
}

export default EmailFormField;
