
export function suppressDefaultBehaviour(event: Event) {
  event.preventDefault();
  event.stopPropagation();
}
