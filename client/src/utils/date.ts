export function formatDate(createdAt: number) {
  let options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  // @ts-ignore
  return new Date(createdAt).toLocaleString('en-US', options);
}
