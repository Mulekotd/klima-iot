"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useAtom } from "jotai";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Icon } from "@/components/icons";
import { authPasswordVisibleAtom } from "@/state/atoms";

const authSchema = z
  .object({
    mode: z.enum(["login", "register"]),
    name: z.string().trim().optional(),
    email: z
      .string()
      .trim()
      .min(1, "Informe seu e-mail.")
      .email("Digite um e-mail válido."),
    password: z.string().min(8, "A senha deve ter pelo menos 8 caracteres."),
    acceptTerms: z.boolean().optional(),
    keepSession: z.boolean().optional(),
  })
  .superRefine((data, context) => {
    if (data.mode !== "register") {
      return;
    }

    if (!data.name || data.name.length < 2) {
      context.addIssue({
        code: "custom",
        message: "Informe seu nome completo.",
        path: ["name"],
      });
    }

    if (!data.acceptTerms) {
      context.addIssue({
        code: "custom",
        message: "Aceite os termos para continuar.",
        path: ["acceptTerms"],
      });
    }
  });

type AuthFormData = z.infer<typeof authSchema>;

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [showPassword, setShowPassword] = useAtom(authPasswordVisibleAtom);
  const router = useRouter();
  const isLogin = mode === "login";
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AuthFormData>({
    resolver: zodResolver(authSchema),
    defaultValues: {
      mode,
      name: "",
      email: "",
      password: "",
      acceptTerms: false,
      keepSession: false,
    },
  });

  function onSubmit() {
    router.push("/dashboard");
  }

  return (
    <form className="auth-form" noValidate onSubmit={handleSubmit(onSubmit)}>
      <input type="hidden" {...register("mode")} />

      {!isLogin && (
        <div className="field">
          <label htmlFor="name">Nome completo</label>
          <input
            aria-describedby={errors.name ? "name-error" : undefined}
            aria-invalid={Boolean(errors.name)}
            autoComplete="name"
            id="name"
            placeholder="Como podemos chamar você?"
            type="text"
            {...register("name")}
          />
          {errors.name && (
            <span className="field-error" id="name-error">
              {errors.name.message}
            </span>
          )}
        </div>
      )}

      <div className="field">
        <label htmlFor="email">E-mail</label>
        <input
          aria-describedby={errors.email ? "email-error" : undefined}
          aria-invalid={Boolean(errors.email)}
          autoComplete="email"
          id="email"
          placeholder="voce@exemplo.com"
          type="email"
          {...register("email")}
        />
        {errors.email && (
          <span className="field-error" id="email-error">
            {errors.email.message}
          </span>
        )}
      </div>

      <div className="field">
        <div className="field-label-row">
          <label htmlFor="password">Senha</label>
          {isLogin && <a href="#recuperar">Esqueci minha senha</a>}
        </div>
        <div className="password-field">
          <input
            aria-describedby={errors.password ? "password-error" : undefined}
            aria-invalid={Boolean(errors.password)}
            autoComplete={isLogin ? "current-password" : "new-password"}
            id="password"
            placeholder={isLogin ? "Digite sua senha" : "Mínimo de 8 caracteres"}
            type={showPassword ? "text" : "password"}
            {...register("password")}
          />
          <button
            aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
            onClick={() => setShowPassword((value) => !value)}
            type="button"
          >
            <Icon name={showPassword ? "eye-off" : "eye"} size={19} />
          </button>
        </div>
        {errors.password && (
          <span className="field-error" id="password-error">
            {errors.password.message}
          </span>
        )}
      </div>

      {!isLogin && (
        <div>
          <label className="checkbox-row">
            <input
              aria-describedby={
                errors.acceptTerms ? "accept-terms-error" : undefined
              }
              aria-invalid={Boolean(errors.acceptTerms)}
              type="checkbox"
              {...register("acceptTerms")}
            />
            <span>
              Eu concordo com os <a href="#termos">Termos de uso</a> e a{" "}
              <a href="#privacidade">Política de privacidade</a>.
            </span>
          </label>
          {errors.acceptTerms && (
            <span className="field-error" id="accept-terms-error">
              {errors.acceptTerms.message}
            </span>
          )}
        </div>
      )}

      {isLogin && (
        <label className="checkbox-row">
          <input type="checkbox" {...register("keepSession")} />
          <span>Manter minha sessão ativa</span>
        </label>
      )}

      <button
        className="button button-primary auth-submit"
        disabled={isSubmitting}
        type="submit"
      >
        {isLogin ? "Entrar na minha conta" : "Criar minha conta"}
        <Icon name="arrow-right" size={18} />
      </button>

      <div className="auth-divider">
        <span>ou continue com</span>
      </div>

      <button className="social-button" type="button">
        <Icon name="google" size={20} />
        Google
      </button>

      <p className="auth-switch">
        {isLogin ? "Ainda não tem uma conta?" : "Já possui uma conta?"}{" "}
        <Link href={isLogin ? "/register" : "/login"}>
          {isLogin ? "Criar conta" : "Entrar"}
        </Link>
      </p>
    </form>
  );
}
