"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User } from "./types";
import { authAPI } from "./api";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (token && storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (data: any) => {
    const res = await authAPI.login(data);
    const payload = res.data as { token?: string; access_token?: string; user: User };
    const token = payload.access_token ?? payload.token;
    if (!token) {
      throw new Error("Authentication response did not include a token");
    }
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(payload.user));
    setUser(payload.user);
  };

  const register = async (data: any) => {
    const res = await authAPI.register(data);
    const payload = res.data as { token?: string; access_token?: string; user: User };
    const token = payload.access_token ?? payload.token;
    if (!token) {
      throw new Error("Authentication response did not include a token");
    }
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(payload.user));
    setUser(payload.user);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
