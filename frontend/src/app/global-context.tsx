'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface GlobalState {
  session: { user_id: number; token: string } | null;
}

interface GlobalContextType {
  state: GlobalState;
  setState: React.Dispatch<React.SetStateAction<GlobalState>>;
}

const GlobalContext = createContext<GlobalContextType | null>(null);

// create the provider component
export const GlobalProvider = ({ children }: { children: ReactNode }) => {
  const [state, setState] = useState<GlobalState>({
    session: null,
  });

  return (
    <GlobalContext.Provider value={{ state, setState }}>
      {children}
    </GlobalContext.Provider>
  );
};

// custom hook to use the global context
export const useGlobalContext = (): GlobalContextType => {
  const context = useContext(GlobalContext);
  if (!context) {
    throw new Error('useGlobalContext must be used within a GlobalProvider');
  }
  return context;
};
