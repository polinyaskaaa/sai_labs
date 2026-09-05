import math
import time
import heapq
from collections import deque

# Повний граф метрополітену Лондона: "Станція": [("Сусідня станція", час_хв), ...]
subway_graph = {'Acton Town': [('Ealing Common', 2), ('South Ealing', 3), ('Turnham Green', 4)],
 'Aldgate': [('Liverpool Street', 3), ('Tower Hill', 2)],
 'Aldgate East': [('Liverpool Street', 2), ('Whitechapel', 2)],
 'Alperton': [('Park Royal', 2), ('Sudbury Town', 3)],
 'Amersham': [('Chalfont & Latimer', 4)],
 'Angel': [("King's Cross", 3), ('Old Street', 3)],
 'Archway': [('Highgate', 3), ('Tufnell Park', 2)],
 'Arnos Grove': [('Bounds Green', 2), ('Southgate', 4)],
 'Arsenal': [('Finsbury Park', 1), ('Holloway Road', 2)],
 'Baker Street': [('Bond Street', 2),
                  ('Edgware Road', 3),
                  ('Finchley Road', 5),
                  ('Great Portland Street', 2),
                  ('Marylebone', 1),
                  ("Regent's Park", 2),
                  ("St. John's Wood", 3)],
 'Balham': [('Clapham South', 2), ('Tooting Bec', 2)],
 'Bank': [('Liverpool Street', 2),
          ('London Bridge', 2),
          ('Monument', 1),
          ('Moorgate', 2),
          ("St. Paul's", 2),
          ('Waterloo', 4)],
 'Barbican': [('Farringdon', 2), ('Moorgate', 2)],
 'Barking': [('East Ham', 3), ('Upney', 2)],
 'Barkingside': [('Fairlop', 2), ('Newbury Park', 2)],
 'Barons Court': [("Earl's Court", 3), ('Hammersmith', 3)],
 'Battersea Power Station': [('Nine Elms', 2)],
 'Bayswater': [('Notting Hill Gate', 2), ('Paddington', 2)],
 'Becontree': [('Dagenham Heathway', 3), ('Upney', 2)],
 'Belsize Park': [('Chalk Farm', 2), ('Hampstead', 2)],
 'Bermondsey': [('Canada Water', 2), ('London Bridge', 2)],
 'Bethnal Green': [('Liverpool Street', 3), ('Mile End', 2)],
 'Blackfriars': [('Mansion House', 2), ('Temple', 1)],
 'Blackhorse Road': [('Tottenham Hale', 2), ('Walthamstow Central', 3)],
 'Bond Street': [('Baker Street', 2), ('Green Park', 2), ('Marble Arch', 1), ('Oxford Circus', 1)],
 'Borough': [('Elephant & Castle', 2), ('London Bridge', 2)],
 'Boston Manor': [('Northfields', 2), ('Osterley', 3)],
 'Bounds Green': [('Arnos Grove', 2), ('Wood Green', 3)],
 'Bow Road': [('Bromley-by-Bow', 2), ('Mile End', 2)],
 'Brent Cross': [('Golders Green', 3), ('Hendon Central', 2)],
 'Brixton': [('Stockwell', 2)],
 'Bromley-by-Bow': [('Bow Road', 2), ('West Ham', 2)],
 'Buckhurst Hill': [('Loughton', 3), ('Woodford', 3)],
 'Burnt Oak': [('Colindale', 2), ('Edgware', 4)],
 'Caledonian Road': [('Holloway Road', 2), ("King's Cross", 3)],
 'Camden Town': [('Chalk Farm', 2), ('Euston', 3), ('Kentish Town', 2), ('Mornington Crescent', 2)],
 'Canada Water': [('Bermondsey', 2), ('Canary Wharf', 3)],
 'Canary Wharf': [('Canada Water', 3), ('North Greenwich', 2)],
 'Canning Town': [('North Greenwich', 3), ('West Ham', 3)],
 'Cannon Street': [('Mansion House', 1), ('Monument', 1)],
 'Canons Park': [('Queensbury', 3), ('Stanmore', 3)],
 'Chalfont & Latimer': [('Amersham', 4), ('Chesham', 9), ('Chorleywood', 4)],
 'Chalk Farm': [('Belsize Park', 2), ('Camden Town', 2)],
 'Chancery Lane': [('Holborn', 1), ("St. Paul's", 2)],
 'Charing Cross': [('Embankment', 1), ('Leicester Square', 1), ('Piccadilly Circus', 2)],
 'Chesham': [('Chalfont & Latimer', 9)],
 'Chigwell': [('Grange Hill', 2), ('Roding Valley', 3)],
 'Chiswick Park': [('Acton Town', 2), ('Turnham Green', 2)],
 'Chorleywood': [('Chalfont & Latimer', 4), ('Rickmansworth', 4)],
 'Clapham Common': [('Clapham North', 2), ('Clapham South', 2)],
 'Clapham North': [('Clapham Common', 2), ('Stockwell', 2)],
 'Clapham South': [('Balham', 2), ('Clapham Common', 2)],
 'Cockfosters': [('Oakwood', 3)],
 'Colindale': [('Burnt Oak', 2), ('Hendon Central', 3)],
 'Colliers Wood': [('South Wimbledon', 2), ('Tooting Broadway', 2)],
 'Covent Garden': [('Holborn', 2), ('Leicester Square', 1)],
 'Croxley': [('Moor Park', 4), ('Watford', 4)],
 'Dagenham East': [('Dagenham Heathway', 2), ('Elm Park', 3)],
 'Dagenham Heathway': [('Becontree', 3), ('Dagenham East', 2)],
 'Debden': [('Loughton', 3), ('Theydon Bois', 3)],
 'Dollis Hill': [('Neasden', 2), ('Willesden Green', 2)],
 'Ealing Broadway': [('Ealing Common', 4), ('West Acton', 3)],
 'Ealing Common': [('Acton Town', 2), ('Ealing Broadway', 4), ('North Ealing', 3)],
 "Earl's Court": [('Barons Court', 3),
                  ('Gloucester Road', 2),
                  ('High Street Kensington', 3),
                  ('Kensington (Olympia)', 3),
                  ('West Brompton', 2),
                  ('West Kensington', 2)],
 'East Acton': [('North Acton', 2), ('White City', 3)],
 'East Finchley': [('Finchley Central', 4), ('Highgate', 3)],
 'East Ham': [('Barking', 3), ('Upton Park', 2)],
 'East Putney': [('Putney Bridge', 3), ('Southfields', 2)],
 'Eastcote': [('Rayners Lane', 2), ('Ruislip Manor', 2)],
 'Edgware': [('Burnt Oak', 4)],
 'Edgware Road': [('Baker Street', 3), ('Marylebone', 2), ('Paddington', 3)],
 'Elephant & Castle': [('Borough', 2), ('Kennington', 2), ('Lambeth North', 2)],
 'Elm Park': [('Dagenham East', 3), ('Hornchurch', 2)],
 'Embankment': [('Charing Cross', 1), ('Temple', 2), ('Waterloo', 2), ('Westminster', 1)],
 'Epping': [('Theydon Bois', 4)],
 'Euston': [('Camden Town', 3), ("King's Cross", 2), ('Mornington Crescent', 2), ('Warren Street', 1)],
 'Euston Square': [('Great Portland Street', 2), ("King's Cross", 2)],
 'Fairlop': [('Barkingside', 2), ('Hainault', 2)],
 'Farringdon': [('Barbican', 2), ("King's Cross", 4)],
 'Finchley Central': [('East Finchley', 4), ('Mill Hill East', 4), ('West Finchley', 2)],
 'Finchley Road': [('Baker Street', 5), ('Swiss Cottage', 2), ('Wembley Park', 7), ('West Hampstead', 1)],
 'Finsbury Park': [('Arsenal', 1), ('Highbury & Islington', 2), ('Manor House', 2), ('Seven Sisters', 4)],
 'Fulham Broadway': [('Parsons Green', 2), ('West Brompton', 2)],
 'Gants Hill': [('Newbury Park', 3), ('Redbridge', 2)],
 'Gloucester Road': [("Earl's Court", 2), ('High Street Kensington', 3), ('South Kensington', 2)],
 'Golders Green': [('Brent Cross', 3), ('Hampstead', 4)],
 'Goldhawk Road': [('Hammersmith', 2), ("Shepherd's Bush Market", 1)],
 'Goodge Street': [('Tottenham Court Road', 1), ('Warren Street', 1)],
 'Grange Hill': [('Chigwell', 2), ('Hainault', 3)],
 'Great Portland Street': [('Baker Street', 2), ('Euston Square', 2)],
 'Green Park': [('Bond Street', 2),
                ('Hyde Park Corner', 2),
                ('Oxford Circus', 2),
                ('Piccadilly Circus', 1),
                ('Victoria', 2),
                ('Westminster', 2)],
 'Greenford': [('Northolt', 2), ('Perivale', 2)],
 'Gunnersbury': [('Kew Gardens', 3), ('Turnham Green', 3)],
 'Hainault': [('Fairlop', 2), ('Grange Hill', 3)],
 'Hammersmith': [('Barons Court', 3), ('Goldhawk Road', 2), ('Turnham Green', 4)],
 'Hampstead': [('Belsize Park', 2), ('Golders Green', 4)],
 'Hanger Lane': [('North Acton', 3), ('Perivale', 3)],
 'Harlesden': [('Stonebridge Park', 2), ('Willesden Junction', 2)],
 'Harrow & Wealdstone': [('Kenton', 2)],
 'Harrow-on-the-Hill': [('North Harrow', 3), ('Northwick Park', 3), ('West Harrow', 2)],
 'Hatton Cross': [('Heathrow Terminals 2 & 3', 4), ('Hounslow West', 4)],
 'Heathrow Terminal 4': [('Heathrow Terminals 2 & 3', 5)],
 'Heathrow Terminal 5': [('Heathrow Terminals 2 & 3', 4)],
 'Heathrow Terminals 2 & 3': [('Hatton Cross', 4), ('Heathrow Terminal 4', 5), ('Heathrow Terminal 5', 4)],
 'Hendon Central': [('Brent Cross', 2), ('Colindale', 3)],
 'High Barnet': [('Totteridge & Whetstone', 3)],
 'High Street Kensington': [("Earl's Court", 3), ('Gloucester Road', 3), ('Notting Hill Gate', 2)],
 'Highbury & Islington': [('Finsbury Park', 2), ("King's Cross", 3)],
 'Highgate': [('Archway', 3), ('East Finchley', 3)],
 'Hillingdon': [('Ickenham', 3), ('Uxbridge', 4)],
 'Holborn': [('Chancery Lane', 1), ('Covent Garden', 2), ('Russell Square', 2), ('Tottenham Court Road', 2)],
 'Holland Park': [('Notting Hill Gate', 2), ("Shepherd's Bush", 2)],
 'Holloway Road': [('Arsenal', 2), ('Caledonian Road', 2)],
 'Hornchurch': [('Elm Park', 2), ('Upminster Bridge', 2)],
 'Hounslow Central': [('Hounslow East', 1), ('Hounslow West', 2)],
 'Hounslow East': [('Hounslow Central', 1), ('Osterley', 2)],
 'Hounslow West': [('Hatton Cross', 4), ('Hounslow Central', 2)],
 'Hyde Park Corner': [('Green Park', 2), ('Knightsbridge', 2)],
 'Ickenham': [('Hillingdon', 3), ('Ruislip', 3)],
 'Kennington': [('Elephant & Castle', 2), ('Nine Elms', 3), ('Oval', 2), ('Waterloo', 3)],
 'Kensal Green': [("Queen's Park", 3), ('Willesden Junction', 3)],
 'Kensington (Olympia)': [("Earl's Court", 3)],
 'Kentish Town': [('Camden Town', 2), ('Tufnell Park', 2)],
 'Kenton': [('Harrow & Wealdstone', 2), ('South Kenton', 2)],
 'Kew Gardens': [('Gunnersbury', 3), ('Richmond', 3)],
 'Kilburn': [('West Hampstead', 2), ('Willesden Green', 2)],
 'Kilburn Park': [('Maida Vale', 2), ("Queen's Park", 2)],
 "King's Cross": [('Angel', 3),
                  ('Baker Street', 5),
                  ('Caledonian Road', 3),
                  ('Euston', 2),
                  ('Farringdon', 4),
                  ('Highbury & Islington', 3),
                  ('Russell Square', 2)],
 'Kingsbury': [('Queensbury', 2), ('Wembley Park', 3)],
 'Knightsbridge': [('Hyde Park Corner', 2), ('South Kensington', 2)],
 'Ladbroke Grove': [('Latimer Road', 2), ('Westbourne Park', 2)],
 'Lambeth North': [('Elephant & Castle', 2), ('Waterloo', 2)],
 'Lancaster Gate': [('Marble Arch', 2), ('Paddington', 3), ('Queensway', 2)],
 'Latimer Road': [('Ladbroke Grove', 2), ('Wood Lane', 2)],
 'Leicester Square': [('Charing Cross', 1),
                      ('Covent Garden', 1),
                      ('Piccadilly Circus', 1),
                      ('Tottenham Court Road', 2)],
 'Leyton': [('Leytonstone', 2), ('Stratford', 3)],
 'Leytonstone': [('Leyton', 2), ('Snaresbrook', 3), ('Wanstead', 2)],
 'Liverpool Street': [('Aldgate', 3), ('Aldgate East', 2), ('Bank', 2), ('Bethnal Green', 3), ('Moorgate', 2)],
 'London Bridge': [('Bank', 2), ('Bermondsey', 2), ('Borough', 2), ('Southwark', 2)],
 'Loughton': [('Buckhurst Hill', 3), ('Debden', 3)],
 'Maida Vale': [('Kilburn Park', 2), ('Warwick Avenue', 1)],
 'Manor House': [('Finsbury Park', 2), ('Turnpike Lane', 4)],
 'Mansion House': [('Blackfriars', 2), ('Cannon Street', 1)],
 'Marble Arch': [('Bond Street', 1), ('Lancaster Gate', 2)],
 'Marylebone': [('Baker Street', 1), ('Paddington', 2)],
 'Mile End': [('Bethnal Green', 2), ('Bow Road', 2), ('Stepney Green', 2), ('Stratford', 4)],
 'Mill Hill East': [('Finchley Central', 4)],
 'Monument': [('Bank', 1), ('Cannon Street', 1), ('Tower Hill', 2)],
 'Moor Park': [('Croxley', 4), ('Northwood', 3), ('Rickmansworth', 4)],
 'Moorgate': [('Bank', 2), ('Barbican', 2), ('Liverpool Street', 2), ('Old Street', 2)],
 'Morden': [('South Wimbledon', 3)],
 'Mornington Crescent': [('Camden Town', 2), ('Euston', 2)],
 'Neasden': [('Dollis Hill', 2), ('Wembley Park', 3)],
 'Newbury Park': [('Barkingside', 2), ('Gants Hill', 3)],
 'Nine Elms': [('Battersea Power Station', 2), ('Kennington', 3)],
 'North Acton': [('East Acton', 2), ('Hanger Lane', 3), ('West Acton', 2)],
 'North Ealing': [('Ealing Common', 3), ('Park Royal', 2)],
 'North Greenwich': [('Canary Wharf', 2), ('Canning Town', 3)],
 'North Harrow': [('Harrow-on-the-Hill', 3), ('Pinner', 3)],
 'North Wembley': [('South Kenton', 2), ('Wembley Central', 2)],
 'Northfields': [('Boston Manor', 2), ('South Ealing', 1)],
 'Northolt': [('Greenford', 2), ('South Ruislip', 3)],
 'Northwick Park': [('Harrow-on-the-Hill', 3), ('Preston Road', 3)],
 'Northwood': [('Moor Park', 3), ('Northwood Hills', 3)],
 'Northwood Hills': [('Northwood', 3), ('Pinner', 3)],
 'Notting Hill Gate': [('Bayswater', 2), ('High Street Kensington', 2), ('Holland Park', 2), ('Queensway', 2)],
 'Oakwood': [('Cockfosters', 3), ('Southgate', 3)],
 'Old Street': [('Angel', 3), ('Moorgate', 2)],
 'Osterley': [('Boston Manor', 3), ('Hounslow East', 2)],
 'Oval': [('Kennington', 2), ('Stockwell', 2)],
 'Oxford Circus': [('Bond Street', 1),
                   ('Green Park', 2),
                   ('Piccadilly Circus', 2),
                   ("Regent's Park", 2),
                   ('Tottenham Court Road', 1),
                   ('Warren Street', 2)],
 'Paddington': [('Bayswater', 2),
                ('Edgware Road', 3),
                ('Lancaster Gate', 3),
                ('Marylebone', 2),
                ('Royal Oak', 1),
                ('Warwick Avenue', 2)],
 'Park Royal': [('Alperton', 2), ('North Ealing', 2)],
 'Parsons Green': [('Fulham Broadway', 2), ('Putney Bridge', 2)],
 'Perivale': [('Greenford', 2), ('Hanger Lane', 3)],
 'Piccadilly Circus': [('Charing Cross', 2), ('Green Park', 1), ('Leicester Square', 1), ('Oxford Circus', 2)],
 'Pimlico': [('Vauxhall', 2), ('Victoria', 2)],
 'Pinner': [('North Harrow', 3), ('Northwood Hills', 3)],
 'Plaistow': [('Upton Park', 2), ('West Ham', 2)],
 'Preston Road': [('Northwick Park', 3), ('Wembley Park', 3)],
 'Putney Bridge': [('East Putney', 3), ('Parsons Green', 2)],
 "Queen's Park": [('Kensal Green', 3), ('Kilburn Park', 2)],
 'Queensbury': [('Canons Park', 3), ('Kingsbury', 2)],
 'Queensway': [('Lancaster Gate', 2), ('Notting Hill Gate', 2)],
 'Rayners Lane': [('Eastcote', 2), ('South Harrow', 4), ('South Ruislip', 5)],
 'Redbridge': [('Gants Hill', 2), ('Wanstead', 2)],
 "Regent's Park": [('Baker Street', 2), ('Oxford Circus', 2)],
 'Richmond': [('Kew Gardens', 3)],
 'Rickmansworth': [('Chorleywood', 4), ('Moor Park', 4)],
 'Roding Valley': [('Chigwell', 3), ('Woodford', 4)],
 'Royal Oak': [('Paddington', 1), ('Westbourne Park', 2)],
 'Ruislip': [('Ickenham', 3), ('Ruislip Manor', 2)],
 'Ruislip Gardens': [('South Ruislip', 2), ('West Ruislip', 3)],
 'Ruislip Manor': [('Eastcote', 2), ('Ruislip', 2)],
 'Russell Square': [('Holborn', 2), ("King's Cross", 2)],
 'Seven Sisters': [('Finsbury Park', 4), ('Tottenham Hale', 2)],
 "Shepherd's Bush": [('Holland Park', 2), ('White City', 3)],
 "Shepherd's Bush Market": [('Goldhawk Road', 1), ('Wood Lane', 2)],
 'Sloane Square': [('South Kensington', 2), ('Victoria', 2)],
 'Snaresbrook': [('Leytonstone', 3), ('South Woodford', 3)],
 'South Ealing': [('Acton Town', 3), ('Northfields', 1)],
 'South Harrow': [('Rayners Lane', 4), ('Sudbury Hill', 3)],
 'South Kensington': [('Gloucester Road', 2), ('Knightsbridge', 2), ('Sloane Square', 2)],
 'South Kenton': [('Kenton', 2), ('North Wembley', 2)],
 'South Ruislip': [('Northolt', 3), ('Ruislip Gardens', 2)],
 'South Wimbledon': [('Colliers Wood', 2), ('Morden', 3)],
 'South Woodford': [('Snaresbrook', 3), ('Woodford', 3)],
 'Southfields': [('East Putney', 2), ('Wimbledon Park', 2)],
 'Southgate': [('Arnos Grove', 4), ('Oakwood', 3)],
 'Southwark': [('London Bridge', 2), ('Waterloo', 2)],
 "St. James's Park": [('Victoria', 2), ('Westminster', 2)],
 "St. John's Wood": [('Baker Street', 3), ('Swiss Cottage', 2)],
 "St. Paul's": [('Bank', 2), ('Chancery Lane', 2)],
 'Stanmore': [('Canons Park', 3)],
 'Stepney Green': [('Mile End', 2), ('Whitechapel', 2)],
 'Stockwell': [('Brixton', 2), ('Clapham North', 2), ('Oval', 2), ('Vauxhall', 3)],
 'Stonebridge Park': [('Harlesden', 2), ('Wembley Central', 2)],
 'Stratford': [('Leyton', 3), ('Mile End', 4), ('West Ham', 3)],
 'Sudbury Hill': [('South Harrow', 3), ('Sudbury Town', 2)],
 'Sudbury Town': [('Alperton', 3), ('Sudbury Hill', 2)],
 'Swiss Cottage': [('Finchley Road', 2), ("St. John's Wood", 2)],
 'Temple': [('Blackfriars', 1), ('Embankment', 2)],
 'Theydon Bois': [('Debden', 3), ('Epping', 4)],
 'Tooting Bec': [('Balham', 2), ('Tooting Broadway', 2)],
 'Tooting Broadway': [('Colliers Wood', 2), ('Tooting Bec', 2)],
 'Tottenham Court Road': [('Goodge Street', 1), ('Holborn', 2), ('Leicester Square', 2), ('Oxford Circus', 1)],
 'Tottenham Hale': [('Blackhorse Road', 2), ('Seven Sisters', 2)],
 'Totteridge & Whetstone': [('High Barnet', 3), ('Woodside Park', 2)],
 'Tower Hill': [('Aldgate', 2), ('Monument', 2)],
 'Tufnell Park': [('Archway', 2), ('Kentish Town', 2)],
 'Turnham Green': [('Acton Town', 4), ('Chiswick Park', 2), ('Hammersmith', 4)],
 'Turnpike Lane': [('Manor House', 4), ('Wood Green', 2)],
 'Upminster': [('Upminster Bridge', 2)],
 'Upminster Bridge': [('Hornchurch', 2), ('Upminster', 2)],
 'Upney': [('Barking', 2), ('Becontree', 2)],
 'Upton Park': [('East Ham', 2), ('Plaistow', 2)],
 'Uxbridge': [('Hillingdon', 4)],
 'Vauxhall': [('Pimlico', 2), ('Stockwell', 3)],
 'Victoria': [('Green Park', 2), ('Pimlico', 2), ('Sloane Square', 2), ("St. James's Park", 2)],
 'Walthamstow Central': [('Blackhorse Road', 3)],
 'Wanstead': [('Leytonstone', 2), ('Redbridge', 2)],
 'Warren Street': [('Euston', 1), ('Goodge Street', 1), ('Oxford Circus', 2)],
 'Warwick Avenue': [('Maida Vale', 1), ('Paddington', 2)],
 'Waterloo': [('Bank', 4),
              ('Embankment', 2),
              ('Kennington', 3),
              ('Lambeth North', 2),
              ('Southwark', 2),
              ('Westminster', 2)],
 'Watford': [('Croxley', 4)],
 'Wembley Central': [('North Wembley', 2), ('Stonebridge Park', 2)],
 'Wembley Park': [('Finchley Road', 7), ('Kingsbury', 3), ('Neasden', 3), ('Preston Road', 3)],
 'West Acton': [('Ealing Broadway', 3), ('North Acton', 2)],
 'West Brompton': [("Earl's Court", 2), ('Fulham Broadway', 2)],
 'West Finchley': [('Finchley Central', 2), ('Woodside Park', 2)],
 'West Ham': [('Bromley-by-Bow', 2), ('Canning Town', 3), ('Plaistow', 2), ('Stratford', 3)],
 'West Hampstead': [('Finchley Road', 1), ('Kilburn', 2)],
 'West Harrow': [('Harrow-on-the-Hill', 2), ('Rayners Lane', 3)],
 'West Kensington': [('Barons Court', 2), ("Earl's Court", 2)],
 'West Ruislip': [('Ruislip Gardens', 3)],
 'Westbourne Park': [('Ladbroke Grove', 2), ('Royal Oak', 2)],
 'Westminster': [('Embankment', 1), ('Green Park', 2), ("St. James's Park", 2), ('Waterloo', 2)],
 'White City': [('East Acton', 3), ("Shepherd's Bush", 3)],
 'Whitechapel': [('Aldgate East', 2), ('Stepney Green', 2)],
 'Willesden Green': [('Dollis Hill', 2), ('Kilburn', 2)],
 'Willesden Junction': [('Harlesden', 2), ('Kensal Green', 3)],
 'Wimbledon': [('Wimbledon Park', 3)],
 'Wimbledon Park': [('Southfields', 2), ('Wimbledon', 3)],
 'Wood Green': [('Bounds Green', 3), ('Turnpike Lane', 2)],
 'Wood Lane': [('Latimer Road', 2), ("Shepherd's Bush Market", 2)],
 'Woodford': [('Buckhurst Hill', 3), ('Roding Valley', 4), ('South Woodford', 3)],
 'Woodside Park': [('Totteridge & Whetstone', 2), ('West Finchley', 2)]}

# Координати станцій на карті (x, y) для розрахунку геометричної відстані
coordinates = {
    "Harrow & Wealdstone": (6, 23), "Kenton": (7, 22), "South Kenton": (7, 21),
    "North Wembley": (7, 20), "Wembley Central": (8, 19), "Stonebridge Park": (9, 18),
    "Harlesden": (9, 17), "Willesden Junction": (10, 16), "Kensal Green": (11, 15),
    "Queen's Park": (12, 15), "Kilburn Park": (13, 14), "Maida Vale": (13, 13),
    "Warwick Avenue": (14, 13), "Paddington": (14, 11), "Marylebone": (16, 12),
    "Baker Street": (17, 12), "Regent's Park": (18, 12), "Oxford Circus": (18, 10),
    "Piccadilly Circus": (19, 9), "Charing Cross": (20, 9), "Embankment": (20, 8),
    "Waterloo": (20, 7), "Lambeth North": (20, 6), "Elephant & Castle": (21, 5),
    "West Ruislip": (1, 22), "Ruislip Gardens": (2, 21), "South Ruislip": (3, 20),
    "Northolt": (4, 19), "Greenford": (5, 18), "Perivale": (6, 17),
    "Hanger Lane": (8, 16), "Ealing Broadway": (7, 12), "West Acton": (8, 13),
    "North Acton": (9, 14), "East Acton": (10, 14), "White City": (11, 13),
    "Shepherd's Bush": (12, 12), "Holland Park": (13, 11), "Notting Hill Gate": (14, 10),
    "Queensway": (15, 10), "Lancaster Gate": (16, 10), "Marble Arch": (17, 10),
    "Bond Street": (17, 10), "Tottenham Court Road": (19, 10), "Holborn": (20, 11),
    "Chancery Lane": (21, 11), "St. Paul's": (22, 11), "Bank": (23, 10),
    "Liverpool Street": (24, 11), "Bethnal Green": (26, 12), "Mile End": (28, 12),
    "Stratford": (30, 13), "Leyton": (31, 14), "Leytonstone": (32, 15),
    "Snaresbrook": (33, 16), "South Woodford": (33, 17), "Woodford": (33, 18),
    "Buckhurst Hill": (33, 20), "Loughton": (33, 21), "Debden": (34, 22),
    "Theydon Bois": (35, 23), "Epping": (36, 24), "Wanstead": (33, 14),
    "Redbridge": (34, 14), "Gants Hill": (35, 14), "Newbury Park": (36, 14),
    "Barkingside": (36, 15), "Fairlop": (36, 16), "Hainault": (36, 17),
    "Grange Hill": (35, 18), "Chigwell": (34, 19), "Roding Valley": (33, 19),
    "Walthamstow Central": (27, 21), "Blackhorse Road": (26, 20), "Tottenham Hale": (25, 20),
    "Seven Sisters": (24, 19), "Finsbury Park": (23, 17), "Highbury & Islington": (22, 15),
    "King's Cross": (21, 13), "Euston": (19, 13), "Warren Street": (18, 11),
    "Green Park": (17, 9), "Victoria": (17, 7), "Pimlico": (18, 6),
    "Vauxhall": (18, 5), "Stockwell": (18, 3), "Brixton": (19, 2),
    "Stanmore": (10, 24), "Canons Park": (11, 23), "Queensbury": (11, 22),
    "Kingsbury": (11, 21), "Wembley Park": (11, 19), "Neasden": (12, 18),
    "Dollis Hill": (13, 17), "Willesden Green": (14, 16), "Kilburn": (14, 15),
    "West Hampstead": (15, 14), "Finchley Road": (15, 13), "Swiss Cottage": (16, 13),
    "St. John's Wood": (16, 12), "Westminster": (19, 8), "Southwark": (21, 7),
    "London Bridge": (23, 8), "Bermondsey": (25, 7), "Canada Water": (26, 7),
    "Canary Wharf": (27, 6), "North Greenwich": (28, 6), "Canning Town": (29, 7),
    "West Ham": (30, 8), "High Barnet": (17, 25), "Totteridge & Whetstone": (17, 24),
    "Woodside Park": (17, 23), "West Finchley": (17, 22), "Mill Hill East": (16, 22),
    "Finchley Central": (17, 21), "East Finchley": (18, 20), "Highgate": (19, 19),
    "Archway": (20, 18), "Tufnell Park": (20, 17), "Kentish Town": (20, 16),
    "Edgware": (12, 24), "Burnt Oak": (12, 23), "Colindale": (13, 22),
    "Hendon Central": (13, 21), "Brent Cross": (14, 20), "Golders Green": (14, 19),
    "Hampstead": (15, 18), "Belsize Park": (16, 17), "Chalk Farm": (17, 16),
    "Camden Town": (18, 15), "Mornington Crescent": (19, 14), "Goodge Street": (19, 11),
    "Angel": (22, 14), "Old Street": (23, 13), "Moorgate": (23, 11),
    "Borough": (22, 7), "Kennington": (20, 4), "Nine Elms": (17, 5),
    "Battersea Power Station": (16, 5), "Oval": (19, 4), "Clapham North": (18, 2),
    "Clapham Common": (17, 1), "Clapham South": (17, 0), "Balham": (17, -1),
    "Tooting Bec": (17, -2), "Tooting Broadway": (17, -3), "Colliers Wood": (17, -4),
    "South Wimbledon": (17, -5), "Morden": (17, -6), "Cockfosters": (25, 25),
    "Oakwood": (25, 24), "Southgate": (25, 23), "Arnos Grove": (24, 22),
    "Bounds Green": (24, 21), "Wood Green": (24, 20), "Turnpike Lane": (24, 19),
    "Manor House": (24, 18), "Arsenal": (23, 16), "Holloway Road": (22, 15),
    "Caledonian Road": (22, 14), "Russell Square": (20, 12), "Covent Garden": (20, 10),
    "Leicester Square": (19, 10), "Hyde Park Corner": (16, 8), "Knightsbridge": (15, 8),
    "South Kensington": (14, 7), "Gloucester Road": (13, 7), "Earl's Court": (12, 7),
    "Barons Court": (10, 7), "Hammersmith": (9, 7), "Turnham Green": (7, 8),
    "Acton Town": (6, 9), "South Ealing": (5, 9), "Northfields": (4, 9),
    "Boston Manor": (3, 9), "Osterley": (2, 9), "Hounslow East": (1, 9),
    "Hounslow Central": (0, 9), "Hounslow West": (-1, 9), "Hatton Cross": (-2, 8),
    "Heathrow Terminals 2 & 3": (-3, 8), "Heathrow Terminal 4": (-3, 7),
    "Heathrow Terminal 5": (-4, 8), "Ealing Common": (6, 11), "North Ealing": (6, 13),
    "Park Royal": (6, 14), "Alperton": (6, 15), "Sudbury Town": (6, 16),
    "Sudbury Hill": (6, 17), "South Harrow": (5, 18), "Rayners Lane": (4, 19),
    "Eastcote": (3, 20), "Ruislip Manor": (2, 21), "Ruislip": (2, 22),
    "Ickenham": (1, 23), "Hillingdon": (0, 23), "Uxbridge": (-1, 23),
    "Richmond": (3, 3), "Kew Gardens": (4, 4), "Gunnersbury": (6, 6),
    "Chiswick Park": (7, 9), "Wimbledon": (11, -3), "Wimbledon Park": (12, -2),
    "Southfields": (13, -1), "East Putney": (13, 1), "Putney Bridge": (13, 3),
    "Parsons Green": (13, 4), "Fulham Broadway": (13, 5), "West Brompton": (12, 6),
    "Kensington (Olympia)": (11, 8), "West Kensington": (11, 7), "High Street Kensington": (13, 9),
    "Bayswater": (14, 10), "Royal Oak": (13, 12), "Westbourne Park": (12, 12),
    "Ladbroke Grove": (11, 13), "Latimer Road": (10, 13), "Wood Lane": (10, 12),
    "Shepherd's Bush Market": (10, 11), "Goldhawk Road": (9, 9), "Sloane Square": (15, 6),
    "St. James's Park": (18, 8), "Temple": (21, 9), "Blackfriars": (22, 9),
    "Mansion House": (23, 9), "Cannon Street": (23, 9), "Monument": (23, 9),
    "Tower Hill": (24, 9), "Aldgate": (24, 10), "Aldgate East": (25, 10),
    "Whitechapel": (26, 10), "Stepney Green": (27, 11), "Bow Road": (29, 12),
    "Bromley-by-Bow": (30, 11), "Plaistow": (31, 10), "Upton Park": (32, 10),
    "East Ham": (33, 10), "Barking": (35, 10), "Upney": (36, 10),
    "Becontree": (37, 10), "Dagenham Heathway": (38, 10), "Dagenham East": (39, 10),
    "Elm Park": (40, 10), "Hornchurch": (41, 10), "Upminster Bridge": (42, 10),
    "Upminster": (43, 10), "Great Portland Street": (17, 11), "Euston Square": (18, 12),
    "Farringdon": (22, 12), "Barbican": (23, 12), "Preston Road": (10, 20),
    "Northwick Park": (9, 21), "Harrow-on-the-Hill": (8, 21), "West Harrow": (7, 20),
    "North Harrow": (7, 22), "Pinner": (6, 23), "Northwood Hills": (5, 24),
    "Northwood": (4, 25), "Moor Park": (3, 26), "Croxley": (2, 27),
    "Watford": (3, 28), "Rickmansworth": (2, 26), "Chorleywood": (1, 27),
    "Chalfont & Latimer": (0, 28), "Chesham": (0, 31), "Amersham": (-1, 29),
    "Edgware Road": (15, 12)
}

def get_neighbors(station):
    """Повертає список доступних суміжних станцій з часом руху"""
    return subway_graph.get(station, [])

def calculate_heuristic(current_station, goal_station):
    """
    Евклідова евристика, поділена на 3.5 для забезпечення допустимості h(n) <= h*(n).
    """
    if current_station not in coordinates or goal_station not in coordinates:
        return 0.0
    x1, y1 = coordinates[current_station]
    x2, y2 = coordinates[goal_station]
    return math.hypot(x1 - x2, y1 - y2) / 3.5


# ============================================================
# НЕІНФОРМОВАНІ АЛГОРИТМИ ПОШУКУ
# ============================================================

def calculate_route_cost(path):
    """Обчислює сумарний час проходження готового маршруту."""
    if not path or len(path) == 1:
        return 0

    total_cost = 0

    for current_station, next_station in zip(path, path[1:]):
        for neighbor, minutes in get_neighbors(current_station):
            if neighbor == next_station:
                total_cost += minutes
                break

    return total_cost


def make_search_result(
    path,
    cost,
    expanded,
    generated,
    max_frontier,
    start_time,
):
    """
    Формує однаковий набір результатів для всіх алгоритмів.
    """
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "found": path is not None,
        "path": path,
        "path_length": len(path) - 1 if path else None,
        "cost": cost,
        "expanded": expanded,
        "generated": generated,
        "max_frontier": max_frontier,
        "time_ms": elapsed_ms,
    }


def bfs_search(start, goal):
    """
    Пошук у ширину (BFS).

    Використовується черга FIFO.
    Алгоритм досліджує граф рівень за рівнем.
    """
    start_time = time.perf_counter()

    queue = deque([(start, [start])])
    visited = {start}

    expanded = 0
    generated = 1
    max_frontier = 1

    while queue:
        current, path = queue.popleft()
        expanded += 1

        if current == goal:
            return make_search_result(
                path,
                calculate_route_cost(path),
                expanded,
                generated,
                max_frontier,
                start_time,
            )

        for neighbor, _ in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

                generated += 1
                max_frontier = max(max_frontier, len(queue))

    return make_search_result(
        None,
        None,
        expanded,
        generated,
        max_frontier,
        start_time,
    )


def dfs_search(start, goal, max_depth):
    """
    Пошук у глибину (DFS) з максимальною глибиною.

    Використовується стек LIFO.
    """
    start_time = time.perf_counter()

    stack = [(start, [start], 0)]

    expanded = 0
    generated = 1
    max_frontier = 1

    while stack:
        current, path, depth = stack.pop()
        expanded += 1

        if current == goal:
            return make_search_result(
                path,
                calculate_route_cost(path),
                expanded,
                generated,
                max_frontier,
                start_time,
            )

        if depth >= max_depth:
            continue

        for neighbor, _ in reversed(get_neighbors(current)):
            # Не повертаємось до вершини,
            # яка вже входить у поточний шлях.
            if neighbor not in path:
                stack.append(
                    (neighbor, path + [neighbor], depth + 1)
                )

                generated += 1
                max_frontier = max(max_frontier, len(stack))

    return make_search_result(
        None,
        None,
        expanded,
        generated,
        max_frontier,
        start_time,
    )


def ucs_search(start, goal):
    """
    Uniform-Cost Search (UCS).

    Використовується пріоритетна черга.
    Пріоритет — накопичена вартість g(n).
    """
    start_time = time.perf_counter()

    priority_queue = [(0, start, [start])]
    best_cost = {start: 0}

    expanded = 0
    generated = 1
    max_frontier = 1

    while priority_queue:
        current_cost, current, path = heapq.heappop(priority_queue)

        # Пропускаємо застарілий дорожчий варіант.
        if current_cost > best_cost.get(current, float("inf")):
            continue

        expanded += 1

        if current == goal:
            return make_search_result(
                path,
                current_cost,
                expanded,
                generated,
                max_frontier,
                start_time,
            )

        for neighbor, minutes in get_neighbors(current):
            new_cost = current_cost + minutes

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor, path + [neighbor])
                )

                generated += 1
                max_frontier = max(
                    max_frontier,
                    len(priority_queue),
                )

    return make_search_result(
        None,
        None,
        expanded,
        generated,
        max_frontier,
        start_time,
    )


# ============================================================
# ЕВРИСТИЧНІ АЛГОРИТМИ ПОШУКУ
# ============================================================

def greedy_search(start, goal):
    """
    Жадібний пошук (Greedy Best-First Search).

    Для вибору вершини використовується тільки h(n).
    """
    start_time = time.perf_counter()

    priority_queue = [
        (calculate_heuristic(start, goal), start, [start])
    ]
    visited = {start}

    expanded = 0
    generated = 1
    max_frontier = 1

    while priority_queue:
        heuristic, current, path = heapq.heappop(priority_queue)
        expanded += 1

        if current == goal:
            return make_search_result(
                path,
                calculate_route_cost(path),
                expanded,
                generated,
                max_frontier,
                start_time,
            )

        for neighbor, _ in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)

                h = calculate_heuristic(neighbor, goal)

                heapq.heappush(
                    priority_queue,
                    (h, neighbor, path + [neighbor])
                )

                generated += 1
                max_frontier = max(
                    max_frontier,
                    len(priority_queue),
                )

    return make_search_result(
        None,
        None,
        expanded,
        generated,
        max_frontier,
        start_time,
    )


def a_star_search(start, goal):
    """
    Алгоритм A*.

    f(n) = g(n) + h(n)
    """
    start_time = time.perf_counter()

    start_h = calculate_heuristic(start, goal)

    priority_queue = [
        (start_h, 0, start, [start])
    ]
    best_cost = {start: 0}

    expanded = 0
    generated = 1
    max_frontier = 1

    while priority_queue:
        f, current_cost, current, path = heapq.heappop(priority_queue)

        # Пропускаємо застарілий дорожчий шлях.
        if current_cost > best_cost.get(current, float("inf")):
            continue

        expanded += 1

        if current == goal:
            return make_search_result(
                path,
                current_cost,
                expanded,
                generated,
                max_frontier,
                start_time,
            )

        for neighbor, minutes in get_neighbors(current):
            new_cost = current_cost + minutes

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost

                h = calculate_heuristic(neighbor, goal)
                new_f = new_cost + h

                heapq.heappush(
                    priority_queue,
                    (
                        new_f,
                        new_cost,
                        neighbor,
                        path + [neighbor],
                    )
                )

                generated += 1
                max_frontier = max(
                    max_frontier,
                    len(priority_queue),
                )

    return make_search_result(
        None,
        None,
        expanded,
        generated,
        max_frontier,
        start_time,
    )


def run_search_algorithm(start, goal, algorithm, max_depth=30):
    """Запускає вибраний алгоритм пошуку."""
    if algorithm == "BFS":
        return bfs_search(start, goal)

    if algorithm == "DFS":
        return dfs_search(start, goal, max_depth)

    if algorithm == "Uniform-Cost Search (UCS)":
        return ucs_search(start, goal)

    if algorithm == "Greedy Best-First Search":
        return greedy_search(start, goal)

    if algorithm == "A*":
        return a_star_search(start, goal)

    raise ValueError(f"Невідомий алгоритм: {algorithm}")


# ============================================================
# ВІЗУАЛІЗАЦІЯ ГРАФА МЕТРО
# ============================================================

def visualize_subway_graph(show_edge_times=False, save_path=None):
    """
    Будує наочний граф мережі метро на основі subway_graph і coordinates.

    Параметри:
    - show_edge_times: якщо True, підписує час руху (хв) на кожному ребрі;
    - save_path: шлях для збереження PNG. Якщо None — лише показує граф.
    """
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    # Унікальні неорієнтовані ребра, щоб не малювати один зв'язок двічі.
    unique_edges = []
    seen_edges = set()
    degree = {station: 0 for station in coordinates}

    for station, neighbors in subway_graph.items():
        if station not in coordinates:
            continue

        for neighbor, minutes in neighbors:
            if neighbor not in coordinates:
                continue

            edge_key = tuple(sorted((station, neighbor)))
            if edge_key in seen_edges:
                continue

            seen_edges.add(edge_key)
            unique_edges.append((station, neighbor, minutes))
            degree[station] += 1
            degree[neighbor] += 1

    # Формуємо відрізки для швидкого малювання ребер.
    segments = []
    for station, neighbor, _ in unique_edges:
        x1, y1 = coordinates[station]
        x2, y2 = coordinates[neighbor]
        segments.append([(x1, y1), (x2, y2)])

    fig, ax = plt.subplots(figsize=(24, 18))

    # Ребра мережі.
    edge_collection = LineCollection(
        segments,
        linewidths=1.0,
        alpha=0.45,
        zorder=1,
    )
    ax.add_collection(edge_collection)

    # Вершини. Більші точки = станції з більшою кількістю зв'язків.
    stations = list(coordinates.keys())
    xs = [coordinates[station][0] for station in stations]
    ys = [coordinates[station][1] for station in stations]
    sizes = [18 + 12 * degree.get(station, 0) for station in stations]

    ax.scatter(xs, ys, s=sizes, zorder=3)

    # Назви станцій.
    for station, (x, y) in coordinates.items():
        ax.annotate(
            station,
            (x, y),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=5.6,
            alpha=0.9,
            zorder=4,
        )

    # За бажанням — час руху між сусідніми станціями.
    if show_edge_times:
        for station, neighbor, minutes in unique_edges:
            x1, y1 = coordinates[station]
            x2, y2 = coordinates[neighbor]
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(minutes),
                fontsize=4.5,
                ha="center",
                va="center",
                zorder=5,
            )

    ax.set_title("Граф мережі Лондонського метро", fontsize=20, pad=18)
    ax.set_xlabel("Координата X")
    ax.set_ylabel("Координата Y")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.15)
    ax.margins(0.03)

    ax.text(
        0.01,
        0.01,
        (
            f"Станцій: {len(coordinates)} | "
            f"Унікальних ребер: {len(unique_edges)} | "
            "Розмір точки ∝ кількості зв'язків"
        ),
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
    )

    if save_path:
        fig.savefig(save_path, dpi=220, bbox_inches="tight")
        print(f"Граф збережено: {save_path}")

    plt.show()





class SubwayGraphApp:
    """
    Сучасний інтерактивний desktop-інтерфейс для графа метро.

    Керування:
    - колесо миші: масштабування;
    - ліва кнопка + перетягування: переміщення;
    - клік по станції: вибір і виділення;
    - пошук: швидкий перехід до станції;
    - перемикач: показати/сховати всі назви.
    """

    # ---------- Палітра ----------
    BG = "#0B1120"
    PANEL = "#111827"
    PANEL_2 = "#172033"
    CARD = "#1E293B"
    BORDER = "#334155"
    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"
    ACCENT = "#38BDF8"
    ACCENT_2 = "#0EA5E9"
    SELECTED = "#FB7185"
    SELECTED_EDGE = "#FFE4E6"
    NODE = "#7DD3FC"
    EDGE = "#64748B"
    GRID = "#334155"
    SUCCESS = "#34D399"
    START_COLOR = "#34D399"
    GOAL_COLOR = "#F97316"
    ROUTE_COLOR = "#FACC15"

    def __init__(self, root):
        import tkinter as tk
        from tkinter import ttk
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        from matplotlib.collections import LineCollection

        self.tk = tk
        self.ttk = ttk
        self.root = root

        self.root.title("London Subway • Graph Explorer")
        self.root.geometry("1500x920")
        self.root.minsize(1050, 700)
        self.root.configure(bg=self.BG)

        # ---------- ttk theme ----------
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "App.TFrame",
            background=self.BG,
        )
        self.style.configure(
            "Panel.TFrame",
            background=self.PANEL,
        )
        self.style.configure(
            "Card.TFrame",
            background=self.CARD,
        )
        self.style.configure(
            "Header.TFrame",
            background=self.PANEL_2,
        )
        self.style.configure(
            "Title.TLabel",
            background=self.PANEL_2,
            foreground=self.TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=self.PANEL_2,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "PanelTitle.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        )
        self.style.configure(
            "Body.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Stat.TLabel",
            background=self.CARD,
            foreground=self.TEXT,
            font=("Segoe UI", 10, "bold"),
        )
        self.style.configure(
            "StatMuted.TLabel",
            background=self.CARD,
            foreground=self.MUTED,
            font=("Segoe UI", 8),
        )

        self.style.configure(
            "Accent.TButton",
            background=self.ACCENT_2,
            foreground="#FFFFFF",
            borderwidth=0,
            focusthickness=0,
            padding=(14, 8),
            font=("Segoe UI", 9, "bold"),
        )
        self.style.map(
            "Accent.TButton",
            background=[
                ("active", self.ACCENT),
                ("pressed", "#0284C7"),
            ],
        )

        self.style.configure(
            "Secondary.TButton",
            background=self.CARD,
            foreground=self.TEXT,
            bordercolor=self.BORDER,
            borderwidth=1,
            padding=(12, 8),
            font=("Segoe UI", 9),
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", self.BORDER)],
        )

        self.style.configure(
            "Modern.TCheckbutton",
            background=self.PANEL_2,
            foreground=self.TEXT,
            font=("Segoe UI", 9),
        )
        self.style.map(
            "Modern.TCheckbutton",
            background=[("active", self.PANEL_2)],
            foreground=[("active", self.TEXT)],
        )

        self.style.configure(
            "Modern.TCombobox",
            fieldbackground=self.CARD,
            background=self.CARD,
            foreground=self.TEXT,
            arrowcolor=self.ACCENT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=6,
        )
        self.style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", self.CARD)],
            foreground=[("readonly", self.TEXT)],
            selectbackground=[("readonly", self.CARD)],
            selectforeground=[("readonly", self.TEXT)],
        )

        # Combobox dropdown colors.
        root.option_add("*TCombobox*Listbox.background", self.CARD)
        root.option_add("*TCombobox*Listbox.foreground", self.TEXT)
        root.option_add("*TCombobox*Listbox.selectBackground", self.ACCENT_2)
        root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

        # ---------- Graph data ----------
        self.stations = sorted(coordinates.keys(), key=str.casefold)
        self.degree = {station: 0 for station in coordinates}
        self.unique_edges = []
        self.seen_edges = set()

        for station, neighbors in subway_graph.items():
            if station not in coordinates:
                continue

            for neighbor, minutes in neighbors:
                if neighbor not in coordinates:
                    continue

                edge_key = tuple(sorted((station, neighbor)))
                if edge_key in self.seen_edges:
                    continue

                self.seen_edges.add(edge_key)
                self.unique_edges.append((station, neighbor, minutes))
                self.degree[station] += 1
                self.degree[neighbor] += 1

        # ---------- Main container ----------
        main = ttk.Frame(root, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True)

        # ---------- Header ----------
        header = ttk.Frame(main, style="Header.TFrame", padding=(18, 12))
        header.pack(fill=tk.X)

        title_block = ttk.Frame(header, style="Header.TFrame")
        title_block.pack(side=tk.LEFT)

        ttk.Label(
            title_block,
            text="LONDON SUBWAY",
            style="Title.TLabel",
        ).pack(anchor="w")

        # ---------- Workspace ----------
        workspace = ttk.Frame(main, style="App.TFrame", padding=(14, 14, 14, 10))
        workspace.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(workspace, style="Panel.TFrame")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        right = ttk.Frame(workspace, style="Panel.TFrame", width=335, padding=(14, 18, 14, 14))
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        # ---------- Route interface ----------
        controls = ttk.Frame(left, style="Header.TFrame", padding=(12, 10))
        controls.pack(fill=tk.X)

        route_row = ttk.Frame(controls, style="Header.TFrame")
        route_row.pack(fill=tk.X)

        ttk.Label(
            route_row,
            text="ВІДПРАВЛЕННЯ",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.start_var = tk.StringVar()
        self.start_box = ttk.Combobox(
            route_row,
            textvariable=self.start_var,
            values=sorted(self.stations),
            width=24,
            style="Modern.TCombobox",
        )
        self.start_box.pack(side=tk.LEFT, padx=(0, 10))
        self.start_box.bind("<<ComboboxSelected>>", self.update_endpoint_markers)

        ttk.Label(
            route_row,
            text="ПРИЗНАЧЕННЯ",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.goal_var = tk.StringVar()
        self.goal_box = ttk.Combobox(
            route_row,
            textvariable=self.goal_var,
            values=sorted(self.stations),
            width=24,
            style="Modern.TCombobox",
        )
        self.goal_box.pack(side=tk.LEFT, padx=(0, 10))
        self.goal_box.bind("<<ComboboxSelected>>", self.update_endpoint_markers)

        ttk.Label(
            route_row,
            text="АЛГОРИТМ",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.algorithm_var = tk.StringVar(value="BFS")
        self.algorithm_box = ttk.Combobox(
            route_row,
            textvariable=self.algorithm_var,
            values=[
                "BFS",
                "DFS",
                "Uniform-Cost Search (UCS)",
                "Greedy Best-First Search",
                "A*",
            ],
            state="readonly",
            width=27,
            style="Modern.TCombobox",
        )
        self.algorithm_box.pack(side=tk.LEFT, padx=(0, 10))
        self.algorithm_box.bind(
            "<<ComboboxSelected>>",
            self.update_algorithm_controls,
        )

        ttk.Label(
            route_row,
            text="MAX DEPTH DFS",
            style="Subtitle.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.max_depth_var = tk.StringVar(value="30")
        self.max_depth_spinbox = ttk.Spinbox(
            route_row,
            from_=1,
            to=300,
            textvariable=self.max_depth_var,
            width=5,
            state="disabled",
        )
        self.max_depth_spinbox.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            route_row,
            text="Знайти маршрут",
            style="Accent.TButton",
            command=self.search_route,
        ).pack(side=tk.LEFT)

        view_row = ttk.Frame(controls, style="Header.TFrame")
        view_row.pack(fill=tk.X, pady=(8, 0))

        ttk.Button(
            view_row,
            text="Очистити вибір",
            style="Secondary.TButton",
            command=self.clear_route_selection,
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(
            view_row,
            text="Скинути вигляд",
            style="Secondary.TButton",
            command=self.reset_view,
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.labels_visible = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            view_row,
            text="Назви станцій",
            variable=self.labels_visible,
            command=self.toggle_labels,
            style="Modern.TCheckbutton",
        ).pack(side=tk.LEFT)

        # ---------- Matplotlib ----------
        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.PANEL)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.BG)

        segments = []
        for station, neighbor, _ in self.unique_edges:
            x1, y1 = coordinates[station]
            x2, y2 = coordinates[neighbor]
            segments.append([(x1, y1), (x2, y2)])

        self.edge_collection = LineCollection(
            segments,
            colors=self.EDGE,
            linewidths=1.15,
            alpha=0.55,
            zorder=1,
        )
        self.ax.add_collection(self.edge_collection)

        # Лінія знайденого маршруту.
        self.route_line, = self.ax.plot(
            [],
            [],
            color=self.ROUTE_COLOR,
            linewidth=4.0,
            alpha=0.95,
            zorder=5,
        )

        # Маркери стартової та кінцевої станції.
        self.start_marker = self.ax.scatter(
            [],
            [],
            s=230,
            marker="o",
            c=self.START_COLOR,
            edgecolors="#ECFDF5",
            linewidths=2.0,
            zorder=8,
        )

        self.goal_marker = self.ax.scatter(
            [],
            [],
            s=300,
            marker="*",
            c=self.GOAL_COLOR,
            edgecolors="#FFF7ED",
            linewidths=1.8,
            zorder=8,
        )

        self.start_label = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(8, 10),
            textcoords="offset points",
            fontsize=8,
            fontweight="bold",
            color="#ECFDF5",
            bbox=dict(
                boxstyle="round,pad=0.30",
                fc=self.CARD,
                ec=self.START_COLOR,
                alpha=0.96,
            ),
            visible=False,
            zorder=9,
        )

        self.goal_label = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(8, 10),
            textcoords="offset points",
            fontsize=8,
            fontweight="bold",
            color="#FFF7ED",
            bbox=dict(
                boxstyle="round,pad=0.30",
                fc=self.CARD,
                ec=self.GOAL_COLOR,
                alpha=0.96,
            ),
            visible=False,
            zorder=9,
        )

        self.xs = [coordinates[s][0] for s in self.stations]
        self.ys = [coordinates[s][1] for s in self.stations]
        self.sizes = [22 + 10 * self.degree.get(s, 0) for s in self.stations]

        self.scatter = self.ax.scatter(
            self.xs,
            self.ys,
            s=self.sizes,
            c=self.NODE,
            edgecolors=self.BG,
            linewidths=0.8,
            alpha=0.96,
            zorder=3,
            picker=True,
        )

        # Station labels.
        self.annotations = {}
        for station, (x, y) in coordinates.items():
            annotation = self.ax.annotate(
                station,
                (x, y),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=6.1,
                color=self.TEXT,
                alpha=0.90,
                zorder=4,
                visible=False,
            )
            self.annotations[station] = annotation

        self.ax.set_title(
            "NETWORK MAP",
            color=self.TEXT,
            fontsize=13,
            fontweight="bold",
            loc="left",
            pad=13,
        )
        self.ax.set_xlabel("X coordinate", color=self.MUTED)
        self.ax.set_ylabel("Y coordinate", color=self.MUTED)

        for spine in self.ax.spines.values():
            spine.set_color(self.BORDER)
            spine.set_linewidth(0.8)

        self.ax.tick_params(colors=self.MUTED, labelsize=8)
        self.ax.grid(
            True,
            color=self.GRID,
            alpha=0.45,
            linewidth=0.6,
            linestyle="--",
        )
        self.ax.set_aspect("equal", adjustable="datalim")
        self.ax.margins(0.04)

        # Initial limits.
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        # Canvas card.
        canvas_frame = ttk.Frame(left, style="Panel.TFrame", padding=(8, 8, 8, 0))
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(
            bg=self.PANEL,
            highlightthickness=0,
            bd=0,
        )
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Toolbar.
        toolbar_frame = tk.Frame(left, bg=self.PANEL_2, height=34)
        toolbar_frame.pack(fill=tk.X)

        self.toolbar = NavigationToolbar2Tk(
            self.canvas,
            toolbar_frame,
            pack_toolbar=False,
        )
        self.toolbar.update()
        self.toolbar.pack(fill=tk.X)
        self._style_toolbar(self.toolbar)

        # ---------- Sidebar ----------

        # Selected station mini-card.
        station_card = ttk.Frame(right, style="Card.TFrame", padding=12)
        station_card.pack(fill=tk.X, pady=(0, 12))

        self.station_name_label = ttk.Label(
            station_card,
            text="Нічого не вибрано",
            style="Stat.TLabel",
            wraplength=270,
        )
        self.station_name_label.pack(anchor="w")

        self.station_meta_label = ttk.Label(
            station_card,
            text="—",
            style="StatMuted.TLabel",
        )
        self.station_meta_label.pack(anchor="w", pady=(5, 0))

        # Detailed info text.
        self.info_text = tk.Text(
            right,
            wrap=tk.WORD,
            height=22,
            state=tk.DISABLED,
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.ACCENT_2,
            selectforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=12,
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # ---------- Tooltip ----------
        self.tooltip = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            color=self.TEXT,
            bbox=dict(
                boxstyle="round,pad=0.45",
                fc=self.CARD,
                ec=self.ACCENT,
                alpha=0.97,
            ),
            arrowprops=dict(
                arrowstyle="->",
                color=self.ACCENT,
            ),
            fontsize=8,
            visible=False,
            zorder=10,
        )

        # ---------- Events ----------
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("pick_event", self.on_pick)

        self.drag_start = None
        self.drag_xlim = None
        self.drag_ylim = None
        self.dragged = False

        self.station_name_label.config(text="Маршрут не вибрано")
        self.station_meta_label.config(text="Оберіть старт, фініш та алгоритм.")

        self.show_info(
            "Пошук маршруту",
            [
                "Реалізовано п'ять алгоритмів:",
                "• BFS — пошук у ширину",
                "• DFS — пошук у глибину",
                "• UCS — пошук за вартістю",
                "• Greedy — пошук за h(n)",
                "• A* — пошук за g(n) + h(n)",
                "",
                "Для DFS можна задати максимальну глибину.",
            ],
        )

    def _make_stat_card(self, parent, value, label, compact=False):
        frame = self.ttk.Frame(parent, style="Card.TFrame", padding=(12, 7))

        value_label = self.ttk.Label(
            frame,
            text=value,
            style="Stat.TLabel",
        )
        value_label.pack(anchor="center" if not compact else "w")

        self.ttk.Label(
            frame,
            text=label,
            style="StatMuted.TLabel",
        ).pack(anchor="center" if not compact else "w")

        return frame

    def _style_toolbar(self, toolbar):
        """Намагається стилізувати стандартний toolbar Matplotlib під dark theme."""
        try:
            toolbar.configure(background=self.PANEL_2)
            for child in toolbar.winfo_children():
                try:
                    child.configure(
                        background=self.PANEL_2,
                        highlightbackground=self.PANEL_2,
                    )
                except Exception:
                    pass
        except Exception:
            pass

    def show_info(self, title, lines):
        self.info_text.config(state=self.tk.NORMAL)
        self.info_text.delete("1.0", self.tk.END)

        self.info_text.tag_configure(
            "title",
            foreground=self.ACCENT,
            font=("Segoe UI", 11, "bold"),
        )
        self.info_text.tag_configure(
            "normal",
            foreground=self.TEXT,
            font=("Segoe UI", 10),
        )
        self.info_text.tag_configure(
            "muted",
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )

        self.info_text.insert(self.tk.END, title + "\n\n", "title")
        self.info_text.insert(self.tk.END, "\n".join(lines), "normal")
        self.info_text.config(state=self.tk.DISABLED)

    def show_station_info(self, station):
        neighbors = subway_graph.get(station, [])

        lines = [
            f"Координати: {coordinates.get(station)}",
            f"Кількість зв'язків: {self.degree.get(station, 0)}",
            "",
            "Сусідні станції:",
        ]

        if neighbors:
            for neighbor, minutes in neighbors:
                lines.append(f"  • {neighbor} — {minutes} хв")
        else:
            lines.append("  Немає даних.")

        self.show_info(station, lines)

    def nearest_station_index(self, event, max_pixels=12):
        if event.x is None or event.y is None:
            return None

        points = self.ax.transData.transform(list(zip(self.xs, self.ys)))

        best_idx = None
        best_dist2 = max_pixels * max_pixels

        for i, (px, py) in enumerate(points):
            dx = px - event.x
            dy = py - event.y
            dist2 = dx * dx + dy * dy
            if dist2 <= best_dist2:
                best_dist2 = dist2
                best_idx = i

        return best_idx

    def on_motion(self, event):
        # Pan.
        if self.drag_start is not None and event.inaxes == self.ax:
            if event.xdata is not None and event.ydata is not None:
                dx = event.xdata - self.drag_start[0]
                dy = event.ydata - self.drag_start[1]

                self.ax.set_xlim(
                    self.drag_xlim[0] - dx,
                    self.drag_xlim[1] - dx,
                )
                self.ax.set_ylim(
                    self.drag_ylim[0] - dy,
                    self.drag_ylim[1] - dy,
                )
                self.dragged = True
                self.canvas.draw_idle()
            return

        if event.inaxes != self.ax:
            if self.tooltip.get_visible():
                self.tooltip.set_visible(False)
                self.canvas.draw_idle()
            return

        idx = self.nearest_station_index(event)

        if idx is None:
            if self.tooltip.get_visible():
                self.tooltip.set_visible(False)
                self.canvas.draw_idle()
            return

        station = self.stations[idx]
        x, y = coordinates[station]

        self.tooltip.xy = (x, y)
        self.tooltip.set_text(
            f"{station}\n"
            f"{self.degree.get(station, 0)} зв'язків"
        )
        self.tooltip.set_visible(True)
        self.canvas.draw_idle()

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return

        base_scale = 1.22

        if event.button == "up":
            scale_factor = 1 / base_scale
        elif event.button == "down":
            scale_factor = base_scale
        else:
            return

        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        xdata = event.xdata
        ydata = event.ydata

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim(
            xdata - new_width * (1 - relx),
            xdata + new_width * relx,
        )
        self.ax.set_ylim(
            ydata - new_height * (1 - rely),
            ydata + new_height * rely,
        )

        self.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax or event.button != 1:
            return

        if event.xdata is None or event.ydata is None:
            return

        if self.nearest_station_index(event, max_pixels=9) is not None:
            self.drag_start = None
            return

        self.drag_start = (event.xdata, event.ydata)
        self.drag_xlim = self.ax.get_xlim()
        self.drag_ylim = self.ax.get_ylim()
        self.dragged = False

    def on_release(self, event):
        self.drag_start = None
        self.drag_xlim = None
        self.drag_ylim = None

    def on_pick(self, event):
        """Клік по станції залишає звичайний перегляд інформації."""
        if event.artist != self.scatter:
            return

        if not event.ind:
            return

        index = event.ind[0]
        station = self.stations[index]

        self.show_station_info(station)

    def resolve_station(self, raw_name):
        """Допоміжний пошук назви станції для інтерфейсу."""
        name = raw_name.strip()

        if name in coordinates:
            return name

        lowered = name.lower()
        matches = [
            station
            for station in self.stations
            if lowered and lowered in station.lower()
        ]

        return matches[0] if matches else None

    def update_endpoint_markers(self, event=None):
        """Показує вибрані старт і фініш без пошуку маршруту."""
        start = self.resolve_station(self.start_var.get())
        goal = self.resolve_station(self.goal_var.get())

        if start:
            self.start_var.set(start)
            x, y = coordinates[start]
            self.start_marker.set_offsets([[x, y]])
            self.start_label.xy = (x, y)
            self.start_label.set_text(f"START: {start}")
            self.start_label.set_visible(True)
        else:
            self.start_marker.set_offsets([])
            self.start_label.set_visible(False)

        if goal:
            self.goal_var.set(goal)
            x, y = coordinates[goal]
            self.goal_marker.set_offsets([[x, y]])
            self.goal_label.xy = (x, y)
            self.goal_label.set_text(f"GOAL: {goal}")
            self.goal_label.set_visible(True)
        else:
            self.goal_marker.set_offsets([])
            self.goal_label.set_visible(False)

        self.canvas.draw_idle()

    def update_algorithm_controls(self, event=None):
        """Максимальна глибина задається тільки для DFS."""
        if self.algorithm_var.get() == "DFS":
            self.max_depth_spinbox.configure(state="normal")
        else:
            self.max_depth_spinbox.configure(state="disabled")

    def search_route(self):
        """Запускає алгоритм і показує всі показники з пункту 8."""
        start = self.resolve_station(self.start_var.get())
        goal = self.resolve_station(self.goal_var.get())
        algorithm = self.algorithm_var.get().strip()

        if not start or not goal:
            self.station_name_label.config(text="Не всі параметри вибрані")
            self.station_meta_label.config(
                text="Вкажіть відправлення і призначення."
            )
            self.show_info(
                "Помилка",
                ["Потрібно вибрати обидві станції."],
            )
            return

        max_depth = 30

        if algorithm == "DFS":
            try:
                max_depth = int(self.max_depth_var.get())
            except ValueError:
                self.show_info(
                    "Помилка",
                    ["Максимальна глибина DFS повинна бути цілим числом."],
                )
                return

            if max_depth < 1:
                self.show_info(
                    "Помилка",
                    ["Максимальна глибина DFS повинна бути не менше 1."],
                )
                return

        self.start_var.set(start)
        self.goal_var.set(goal)
        self.update_endpoint_markers()

        result = run_search_algorithm(
            start,
            goal,
            algorithm,
            max_depth,
        )

        path = result["path"]

        if not result["found"]:
            self.route_line.set_data([], [])

            self.station_name_label.config(text="Маршрут не знайдено")
            self.station_meta_label.config(text=f"Алгоритм: {algorithm}")

            result_lines = [
                f"Розв'язок знайдено: Ні",
                f"Відправлення: {start}",
                f"Призначення: {goal}",
                f"Алгоритм: {algorithm}",
            ]

            if algorithm == "DFS":
                result_lines.append(
                    f"Максимальна глибина DFS: {max_depth}"
                )

            result_lines.extend([
                f"Розгорнутих станів: {result['expanded']}",
                f"Сформованих станів: {result['generated']}",
                f"Макс. розмір frontier: {result['max_frontier']}",
                f"Час виконання: {result['time_ms']:.6f} мс",
                "",
                "За заданих параметрів шлях не знайдено.",
            ])

            self.show_info("Результат пошуку", result_lines)
            self.canvas.draw_idle()
            return

        route_x = [coordinates[station][0] for station in path]
        route_y = [coordinates[station][1] for station in path]
        self.route_line.set_data(route_x, route_y)

        self.station_name_label.config(text=f"{start} → {goal}")
        self.station_meta_label.config(
            text=(
                f"{algorithm} • "
                f"{result['cost']} хв • "
                f"{result['path_length']} переходів"
            )
        )

        result_lines = [
            "Розв'язок знайдено: Так",
            f"Алгоритм: {algorithm}",
        ]

        if algorithm == "DFS":
            result_lines.append(
                f"Максимальна глибина DFS: {max_depth}"
            )

        result_lines.extend([
            f"Довжина шляху: {result['path_length']} переходів",
            f"Кількість станцій у шляху: {len(path)}",
            f"Сумарна вартість: {result['cost']} хв",
            f"Розгорнутих станів: {result['expanded']}",
            f"Сформованих станів: {result['generated']}",
            f"Макс. розмір frontier: {result['max_frontier']}",
            f"Час виконання: {result['time_ms']:.6f} мс",
            "",
            "Маршрут:",
        ])

        for number, station in enumerate(path, start=1):
            result_lines.append(f"{number}. {station}")

        self.show_info("Маршрут знайдено", result_lines)
        self.fit_route_to_view(path)
        self.canvas.draw_idle()

    def fit_route_to_view(self, path):
        """Масштабує граф навколо знайденого маршруту."""
        if not path:
            return

        xs = [coordinates[station][0] for station in path]
        ys = [coordinates[station][1] for station in path]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = max(max_x - min_x, 2)
        height = max(max_y - min_y, 2)

        margin_x = max(1.5, width * 0.15)
        margin_y = max(1.5, height * 0.15)

        self.ax.set_xlim(min_x - margin_x, max_x + margin_x)
        self.ax.set_ylim(min_y - margin_y, max_y + margin_y)

    def clear_route_selection(self):
        """Повністю очищає стартову та кінцеву мітки і вибрані значення."""
        self.start_var.set("")
        self.goal_var.set("")
        self.algorithm_var.set("BFS")
        self.max_depth_var.set("30")
        self.update_algorithm_controls()

        # Прибираємо знайдений маршрут.
        self.route_line.set_data([], [])

        # Прибираємо мітки START / GOAL.
        self.start_marker.set_offsets([])
        self.goal_marker.set_offsets([])

        # Прибираємо підписи біля них.
        self.start_label.set_text("")
        self.goal_label.set_text("")
        self.start_label.set_visible(False)
        self.goal_label.set_visible(False)

        self.station_name_label.config(text="Маршрут не вибрано")
        self.station_meta_label.config(text="Оберіть старт, фініш та алгоритм.")

        self.show_info(
            "Параметри маршруту",
            [
                "Мітки очищено.",
                "",
                "Оберіть точку відправлення.",
                "Оберіть пункт призначення.",
                "Оберіть алгоритм пошуку.",
            ],
        )

        self.canvas.draw_idle()

    def reset_view(self):
        self.ax.set_xlim(self.initial_xlim)
        self.ax.set_ylim(self.initial_ylim)
        self.canvas.draw_idle()

    def toggle_labels(self):
        visible = self.labels_visible.get()

        for annotation in self.annotations.values():
            annotation.set_visible(visible)

        self.canvas.draw_idle()


def run_subway_gui():
    import tkinter as tk

    root = tk.Tk()
    SubwayGraphApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_subway_gui()
