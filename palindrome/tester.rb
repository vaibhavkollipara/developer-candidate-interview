class Tester

    class T1
        def palindrome(string)
            # first implementation
            if not string.is_a? String or string.empty?
              return false
            end
            string.gsub!(/[^0-9A-Za-z]/, '')
            string = string.downcase
            if string.empty?
                return false
            end
            start_index = 0
            end_index = (string.length) -1
            while start_index <= end_index do
                if string[start_index].chr != string[end_index].chr
                  return false
                end
                start_index += 1
                end_index += 1
                return true
            end
        end
    end

    class T2
        def palindrome(string)
          # second implementation
          if not string.is_a? String or string.empty?
              return false
          end
          string.gsub!(/[^0-9A-Za-z]/, '')
          string = string.downcase
          if string.empty?
            return false
          end
          return string == string.reverse
        end
    end

end
