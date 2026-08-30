# What we can verify at SWOSU

## NOT VERIFIED FOR SWOSU TENANT

This public-source run did not use an authenticated student session and did
not inspect private tenant screens, student data, or account identifiers.
Therefore we cannot prove the exact product label after QuickLaunch, whether
the account is Entra-backed, whether an EDP shield is shown, which license is
assigned, which model selector choices are visible, whether OpenAI or Anthropic
is enabled, whether Work IQ is available, or what local notice/terms link the
tenant presents.

Microsoft-wide documentation is not evidence of SWOSU-specific enablement.
The safe classroom statement is: a SWOSU student may be entering a
Microsoft-hosted organizational Copilot experience through institutional SSO,
but the exact SWOSU tenant configuration remains unverified here.

To verify later without exposing student data, record only the public product
label, generic protection indicator, and model names visible in a redacted
screen or instructor-owned test account. Do not commit tokens, names, email
addresses, private tenant identifiers, prompts, or screenshots containing
student/organizational data.
