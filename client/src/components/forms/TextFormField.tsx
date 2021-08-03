import React from 'react';
import { FormControl, FormLabel, Input } from '@chakra-ui/react';

interface TextFormFieldProps {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FormEvent) => void;
}

function TextFormField({ label, value, onChange, onBlur }: TextFormFieldProps) {
  return (
    <FormControl className="formControl">
      <FormLabel>{label}</FormLabel>
      <Input
        type="text"
        placeholder={label.toLowerCase()}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
      />
    </FormControl>
  );
}

export default TextFormField;
