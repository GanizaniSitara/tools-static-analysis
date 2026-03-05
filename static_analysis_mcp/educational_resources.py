"""Educational resources for code smell types.

Provides curated YouTube videos and documentation links to help developers
understand and learn how to fix various code smells and vulnerabilities.
"""

from typing import Dict, List, Any

# Curated YouTube videos for each smell type
EDUCATIONAL_VIDEOS = {
    "sql_injection": [
        {
            "title": "SQL Injection Explained - OWASP Top 10",
            "url": "https://www.youtube.com/watch?v=ciNHn38EyRc",
            "channel": "PwnFunction",
            "duration": "12:34",
            "topics": ["SQL injection", "Parameterized queries", "Security"]
        },
        {
            "title": "Preventing SQL Injection in .NET",
            "url": "https://www.youtube.com/watch?v=_jKylhJtPmI",
            "channel": "dotnet",
            "duration": "18:45",
            "topics": ["ADO.NET", "Entity Framework", "Parameters"]
        }
    ],
    "exception_swallowing": [
        {
            "title": "Exception Handling Best Practices - C#",
            "url": "https://www.youtube.com/watch?v=2r1Ly2j86Mg",
            "channel": "Nick Chapsas",
            "duration": "15:23",
            "topics": ["Try-catch", "Error handling", "Logging"]
        },
        {
            "title": "Why Empty Catch Blocks Are Bad",
            "url": "https://www.youtube.com/watch?v=lw-jl9kN8Ek",
            "channel": "CodeOpinion",
            "duration": "8:12",
            "topics": ["Exception handling", "Error logging", "Best practices"]
        }
    ],
    "sync_over_async": [
        {
            "title": "Async/Await Deadlock Explained",
            "url": "https://www.youtube.com/watch?v=_1Zva76Eqvs",
            "channel": "Raw Coding",
            "duration": "22:10",
            "topics": ["ConfigureAwait", "Deadlock", "Task.Result"]
        },
        {
            "title": "Async Best Practices - Don't Block",
            "url": "https://www.youtube.com/watch?v=_3gm1gB-dDM",
            "channel": "Nick Chapsas",
            "duration": "16:30",
            "topics": ["Async patterns", "Blocking", "Performance"]
        }
    ],
    "command_injection": [
        {
            "title": "Command Injection Attacks Explained",
            "url": "https://www.youtube.com/watch?v=0Yj_ECXH5l4",
            "channel": "LiveOverflow",
            "duration": "16:45",
            "topics": ["Shell injection", "Input sanitization", "Security"]
        },
        {
            "title": "Preventing OS Command Injection",
            "url": "https://www.youtube.com/watch?v=IAmATesDG8k",
            "channel": "OWASP Foundation",
            "duration": "12:20",
            "topics": ["Input validation", "Command execution", "Security"]
        }
    ],
    "open_redirect": [
        {
            "title": "Open Redirect Vulnerability Tutorial",
            "url": "https://www.youtube.com/watch?v=4Jk_I-cw4WE",
            "channel": "OWASP",
            "duration": "10:30",
            "topics": ["URL validation", "Redirect security", "Phishing"]
        },
        {
            "title": "Understanding Open Redirects",
            "url": "https://www.youtube.com/watch?v=6i1dZouTxvA",
            "channel": "PwnFunction",
            "duration": "8:45",
            "topics": ["URL manipulation", "Security risks"]
        }
    ],
    "hardcoded_secret": [
        {
            "title": "Never Store Secrets in Code - Best Practices",
            "url": "https://www.youtube.com/watch?v=_lPvYfvLTwY",
            "channel": "Nick Chapsas",
            "duration": "14:15",
            "topics": ["Secrets management", "Environment variables", "Security"]
        },
        {
            "title": "Managing Secrets in .NET Applications",
            "url": "https://www.youtube.com/watch?v=PkLLP2tcd28",
            "channel": "dotnet",
            "duration": "18:30",
            "topics": ["User Secrets", "Azure Key Vault", "Configuration"]
        }
    ],
    "weak_crypto": [
        {
            "title": "Cryptography Best Practices",
            "url": "https://www.youtube.com/watch?v=2aHkqB2-46k",
            "channel": "Computerphile",
            "duration": "20:15",
            "topics": ["Encryption", "Hashing", "Cryptographic algorithms"]
        },
        {
            "title": "Secure Cryptography in .NET",
            "url": "https://www.youtube.com/watch?v=NjS_s5mG6KQ",
            "channel": "dotnet",
            "duration": "16:45",
            "topics": ["AES", "SHA256", "Crypto libraries"]
        }
    ],
    "god_method": [
        {
            "title": "Code Smells: Long Methods",
            "url": "https://www.youtube.com/watch?v=VhYuW0dsclY",
            "channel": "CodeAesthetic",
            "duration": "12:40",
            "topics": ["Refactoring", "Single Responsibility", "Method extraction"]
        },
        {
            "title": "Refactoring God Methods",
            "url": "https://www.youtube.com/watch?v=7ZmzwS1rKY0",
            "channel": "Industrial Logic",
            "duration": "15:30",
            "topics": ["Method decomposition", "Clean code"]
        }
    ],
    "deep_nesting": [
        {
            "title": "Reducing Nested If Statements",
            "url": "https://www.youtube.com/watch?v=CFRhGnuXG-4",
            "channel": "CodeAesthetic",
            "duration": "10:20",
            "topics": ["Guard clauses", "Early returns", "Code readability"]
        },
        {
            "title": "Flattening Arrow Code",
            "url": "https://www.youtube.com/watch?v=cFAo7VTwAl8",
            "channel": "Nick Chapsas",
            "duration": "13:15",
            "topics": ["Cyclomatic complexity", "Refactoring"]
        }
    ],
    "magic_number": [
        {
            "title": "Why Magic Numbers Are Bad",
            "url": "https://www.youtube.com/watch?v=wXkCz9FqT8I",
            "channel": "Web Dev Simplified",
            "duration": "8:30",
            "topics": ["Named constants", "Code maintainability"]
        },
        {
            "title": "Clean Code: Magic Numbers and Constants",
            "url": "https://www.youtube.com/watch?v=zqh7WzS2bBo",
            "channel": "CodeOpinion",
            "duration": "11:45",
            "topics": ["Enums", "Const variables", "Best practices"]
        }
    ],
    "path_traversal": [
        {
            "title": "Path Traversal Vulnerability Explained",
            "url": "https://www.youtube.com/watch?v=5jHRN2FnLto",
            "channel": "LiveOverflow",
            "duration": "14:25",
            "topics": ["Directory traversal", "Input validation", "File security"]
        },
        {
            "title": "Preventing Path Traversal Attacks",
            "url": "https://www.youtube.com/watch?v=k1RNQ7qRvWo",
            "channel": "OWASP",
            "duration": "10:50",
            "topics": ["Path sanitization", "Security controls"]
        }
    ],
    "xss": [
        {
            "title": "Cross-Site Scripting (XSS) Explained",
            "url": "https://www.youtube.com/watch?v=EoaDgUgS6QA",
            "channel": "PwnFunction",
            "duration": "13:40",
            "topics": ["XSS attacks", "Input sanitization", "Output encoding"]
        },
        {
            "title": "Preventing XSS in Web Applications",
            "url": "https://www.youtube.com/watch?v=ns1LX6mEvyM",
            "channel": "OWASP",
            "duration": "18:20",
            "topics": ["Content Security Policy", "HTML encoding"]
        }
    ],
    "csrf": [
        {
            "title": "CSRF Attacks Explained",
            "url": "https://www.youtube.com/watch?v=vRBihr41JTo",
            "channel": "PwnFunction",
            "duration": "11:15",
            "topics": ["Cross-Site Request Forgery", "Anti-CSRF tokens"]
        },
        {
            "title": "Implementing CSRF Protection",
            "url": "https://www.youtube.com/watch?v=m0EHlfTgGUU",
            "channel": "Hussein Nasser",
            "duration": "16:40",
            "topics": ["Token validation", "SameSite cookies"]
        }
    ],
    "insecure_deserialization": [
        {
            "title": "Insecure Deserialization Explained",
            "url": "https://www.youtube.com/watch?v=t-zVC-CxYjw",
            "channel": "LiveOverflow",
            "duration": "17:30",
            "topics": ["Serialization", "Object injection", "Security"]
        },
        {
            "title": "Secure Deserialization in .NET",
            "url": "https://www.youtube.com/watch?v=oxlD8VWWHE8",
            "channel": "OWASP",
            "duration": "14:20",
            "topics": ["Type validation", "Safe parsers"]
        }
    ],
    "xxe": [
        {
            "title": "XML External Entity (XXE) Attack",
            "url": "https://www.youtube.com/watch?v=gjm6VHZa_8s",
            "channel": "PwnFunction",
            "duration": "12:50",
            "topics": ["XML parsing", "External entities", "Security"]
        },
        {
            "title": "Preventing XXE Vulnerabilities",
            "url": "https://www.youtube.com/watch?v=CWeWD_6aRvA",
            "channel": "OWASP",
            "duration": "15:10",
            "topics": ["XML parser configuration", "Entity expansion"]
        }
    ]
}

DOCUMENTATION_LINKS = {
    "sql_injection": [
        "https://owasp.org/www-community/attacks/SQL_Injection",
        "https://learn.microsoft.com/en-us/sql/connect/ado-net/sql/sql-injection",
        "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
    ],
    "exception_swallowing": [
        "https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions",
        "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/",
        "https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.logging"
    ],
    "sync_over_async": [
        "https://learn.microsoft.com/en-us/archive/msdn-magazine/2015/july/async-programming-brownfield-async-development",
        "https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/",
        "https://blog.stephencleary.com/2012/07/dont-block-on-async-code.html"
    ],
    "command_injection": [
        "https://owasp.org/www-community/attacks/Command_Injection",
        "https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/78.html"
    ],
    "open_redirect": [
        "https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html",
        "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/04-Testing_for_Client-side_URL_Redirect",
        "https://cwe.mitre.org/data/definitions/601.html"
    ],
    "hardcoded_secret": [
        "https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets",
        "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/798.html"
    ],
    "weak_crypto": [
        "https://learn.microsoft.com/en-us/dotnet/standard/security/cryptography-model",
        "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/327.html"
    ],
    "god_method": [
        "https://refactoring.guru/smells/long-method",
        "https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-values",
        "https://martinfowler.com/bliki/FunctionLength.html"
    ],
    "deep_nesting": [
        "https://refactoring.guru/smells/indecent-exposure",
        "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502",
        "https://martinfowler.com/bliki/CyclomaticComplexity.html"
    ],
    "magic_number": [
        "https://refactoring.guru/smells/magic-numbers",
        "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/const",
        "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum"
    ],
    "path_traversal": [
        "https://owasp.org/www-community/attacks/Path_Traversal",
        "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/22.html"
    ],
    "xss": [
        "https://owasp.org/www-community/attacks/xss/",
        "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html",
        "https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting"
    ],
    "csrf": [
        "https://owasp.org/www-community/attacks/csrf",
        "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html",
        "https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery"
    ],
    "insecure_deserialization": [
        "https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data",
        "https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/502.html"
    ],
    "xxe": [
        "https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing",
        "https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html",
        "https://cwe.mitre.org/data/definitions/611.html"
    ]
}


def get_educational_resources(smell_type: str) -> Dict[str, Any]:
    """Get curated educational resources for a smell type.

    Args:
        smell_type: Type of code smell (e.g., 'sql_injection', 'exception_swallowing')

    Returns:
        Dictionary containing:
        - smell_type: The smell type queried
        - educational_videos: List of video resources (max 3)
        - documentation_links: List of documentation URLs
        - has_resources: Boolean indicating if specific resources exist
    """
    # Normalize smell type (handle variations)
    normalized_type = smell_type.lower().replace('-', '_').replace(' ', '_')

    videos = EDUCATIONAL_VIDEOS.get(normalized_type, [])
    docs = DOCUMENTATION_LINKS.get(normalized_type, [])

    # Fallback to generic resources if no specific ones
    if not videos and not docs:
        videos = [
            {
                "title": f"Understanding {smell_type.replace('_', ' ').title()}",
                "url": f"https://www.youtube.com/results?search_query={smell_type.replace('_', '+')}+tutorial",
                "channel": "YouTube Search",
                "duration": "N/A",
                "note": "Generic search results - review top videos"
            }
        ]
        docs = [
            f"https://www.google.com/search?q={smell_type.replace('_', '+')}+best+practices"
        ]

    return {
        "smell_type": smell_type,
        "educational_videos": videos[:3],  # Return max 3 videos
        "documentation_links": docs,
        "has_resources": bool(EDUCATIONAL_VIDEOS.get(normalized_type) or DOCUMENTATION_LINKS.get(normalized_type)),
        "related_topics": [topic for video in videos[:3] for topic in video.get('topics', [])]
    }
