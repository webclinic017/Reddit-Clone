import React from 'react';
import { FormControl, FormLabel, Input } from '@chakra-ui/react';

interface PasswordFormFieldProps {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FormEvent) => void;
}

function PasswordFormField({
  label,
  value,
  onChange,
  onBlur,
}: PasswordFormFieldProps) {
  return (
    <FormControl className="formControl">
      <FormLabel>{label}</FormLabel>
      <Input
        type="password"
        placeholder={label.toLowerCase()}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
      />
    </FormControl>
  );
}

export default PasswordFormField;
