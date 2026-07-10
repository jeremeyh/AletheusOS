import {
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import {
  useState,
  type ReactNode,
} from "react";

export function RuntimeQueryProvider({
  children,
}: {
  readonly children: ReactNode;
}) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: 1,
      },
      mutations: {
        retry: 0,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
